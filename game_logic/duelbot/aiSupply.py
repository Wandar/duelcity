# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from KBEngine import *

"""
aiSupply: CardSupply — the only place allowed to source cards outside the normal draw.

Principle: NEVER create cards out of thin air onto the field (the opponent
would notice the hand count not dropping). Instead, rewrite the identity of a
card the human player has NEVER seen (hand card = only a card back to them,
deck card = only a count), then let the bot play it through the normal flow.

Facts this relies on (Game.modifyCardList):
  - hand      sendType=1  -> full card data only sent to its owner
  - deck      sendType=0  -> only the count is sent
  - field/grave/banish sendType=2 -> public; once a card has been there the
    player may remember it, so it is marked revealed and never morphed again.

The two y_ entry points follow the justCheck convention used by y_think.
"""


def AI_MSG(*s):
    if True:
        DEBUG_MSG(*s)


class CardSupply(Reload):
    CARD_CREATE_LIMIT = 3  # hard cap of total copies per cardKey (deck copies included)

    def __init__(self, bot):
        Reload.__init__(self, True, False)
        self.bot = bot
        self.revealedIDs = set()      # uniIDs the human player has ever seen
        self.cardCreatedCount = {}    # cardKey -> total copies existing/created

    # ============================================================
    # Copy counting (seeded from the configured deck)
    # ============================================================
    def initFromConfig(self, config):
        self.revealedIDs = set()
        self.cardCreatedCount = {}
        deck = config.get("deck") or {}
        if isinstance(deck, dict):
            for groupKey, cardList in deck.items():
                if not isinstance(cardList, (list, tuple)):
                    continue
                for cardKey in cardList:
                    self.cardCreatedCount[cardKey] = self.cardCreatedCount.get(cardKey, 0) + 1
        elif isinstance(deck, (list, tuple)):
            for cardKey in deck:
                self.cardCreatedCount[cardKey] = self.cardCreatedCount.get(cardKey, 0) + 1

    def canCreateMore(self, cardKey) -> bool:
        return self.cardCreatedCount.get(cardKey, 0) < self.CARD_CREATE_LIMIT

    def onCreate(self, cardKey):
        self.cardCreatedCount[cardKey] = self.cardCreatedCount.get(cardKey, 0) + 1

    def pickCreatableFromPool(self, pool):
        """Random cardKey from pool that is still under the copy cap; None if all capped."""
        if not pool:
            return None
        candidates = [k for k in pool if self.canCreateMore(k)]
        if not candidates:
            return None
        return random.choice(candidates)

    # ============================================================
    # Reveal tracking
    # ============================================================
    def onSignal(self, signal):
        """Mark cards as revealed once they enter a public zone.

        Conservative: face-down set cards entering the field are also marked
        (we merely lose a morph candidate, never leak information)."""
        names = signal.getSelfAndFatherSignalNames()
        if ("EnterField" in names or "EnterGrave" in names or "EnterBanished" in names):
            card = signal.card
            if card is not None:
                self.revealedIDs.add(card.uniID)

    def isHidden(self, card) -> bool:
        """True if the human player can NOT know this card's identity."""
        if card.uniID in self.revealedIDs:
            return False
        return card.location in (LOCATION.hand, LOCATION.deck)

    def hiddenCards(self, location) -> List[Card]:
        game = self.bot.game
        side = self.bot.getSide()
        if location == LOCATION.hand:
            cardList = game.hands[side]
        elif location == LOCATION.deck:
            cardList = game.decks[side]
        else:
            return []
        return [c for c in cardList if self.isHidden(c)]

    # ============================================================
    # Core: in-place identity rewrite
    # ============================================================
    def morph(self, oldCard, newKey):
        """Rewrite a hidden hand/deck card into `newKey`.

        Cards are per-cardKey Python classes, so we must create a fresh
        instance of the target class. The new card inherits the old card's
        uniID so modifyCardList(change=0) swaps it in place: the opponent's
        client sees no change at all (card back / deck count only).
        Returns the new Card or None."""
        game = self.bot.game
        loc = oldCard.location
        if loc not in (LOCATION.hand, LOCATION.deck):
            return None
        if not self.isHidden(oldCard):
            return None
        if not self.canCreateMore(newKey):
            return None

        side = oldCard.side
        newCard = game.createCard(newKey, side)
        if not newCard:
            return None

        # Inherit the old identity slot: same uniID, same list position.
        del game.duel.usedCards[newCard.uniID]
        newCard.uniID = oldCard.uniID
        game.duel.usedCards[oldCard.uniID] = newCard
        self.onCreate(newKey)
        game.modifyCardList(side, loc, 0, newCard)  # in-place swap by uniID

        AI_MSG("[supply] morph", oldCard.cardKey, "->", newKey, "at", loc)
        return newCard

    # ============================================================
    # Providers
    # ============================================================
    def _morphCandidatesInHand(self, protectKeys):
        """Hidden hand cards we may sacrifice, cheapest first.
        Cards whose key is in protectKeys are excluded (they are the very
        cards a combo counts on having)."""
        protect = set(protectKeys or ())
        cands = [c for c in self.hiddenCards(LOCATION.hand) if c.cardKey not in protect]
        cands.sort(key=lambda c: self.bot._scoreCard(c, True))
        return cands

    def canProvideToHand(self, missingKeys) -> bool:
        if not missingKeys:
            return False
        need = {}
        for k in missingKeys:
            need[k] = need.get(k, 0) + 1
        for k, n in need.items():
            if self.cardCreatedCount.get(k, 0) + n > self.CARD_CREATE_LIMIT:
                return False
        return len(self._morphCandidatesInHand(missingKeys)) >= len(missingKeys)

    def provideToHand(self, missingKeys) -> bool:
        """Morph hidden hand cards into `missingKeys`. All-or-nothing."""
        if not self.canProvideToHand(missingKeys):
            return False
        cands = self._morphCandidatesInHand(missingKeys)
        for key, victim in zip(missingKeys, cands):
            if self.morph(victim, key) is None:
                return False
        return True

    def provideOnDeckTop(self, key):
        """Morph a hidden deck card into `key` and move it to the deck top,
        so a normal draw fetches it. Returns the Card or None."""
        game = self.bot.game
        side = self.bot.getSide()
        deck = game.decks[side]
        if not deck:
            return None

        # Prefer the current top card: no reordering needed at all.
        top = deck[-1]
        victim = top if self.isHidden(top) else None
        if victim is None:
            hidden = self.hiddenCards(LOCATION.deck)
            if not hidden:
                return None
            victim = random.choice(hidden)

        newCard = self.morph(victim, key)
        if newCard is None:
            return None

        if deck and deck[-1] is not newCard:
            # Move to top via the sanctioned list API (count-only sync for decks).
            game.modifyCardList(side, LOCATION.deck, -1, newCard)
            game.modifyCardList(side, LOCATION.deck, 1, newCard,
                                returnToDeckType=RETURN_TO_DECK.top)
        return newCard

    # ============================================================
    # justCheck entry points used by y_think
    # ============================================================
    def y_fillSmall(self, justCheck):
        """Put one more small monster on board without creating cards from
        thin air. Preferred: morph a hidden HAND card and summon it (hand
        count drops naturally). Fallback: morph a hidden deck card to the
        top and draw it."""
        bot = self.bot
        game = bot.game
        side = bot.getSide()

        if game.freeMonsterSpace(side) <= 0:
            return False
        key = bot._pickLowLevelMonsterKey(justPeek=justCheck)
        if not key:
            return False
        handVictims = self._morphCandidatesInHand([key])
        deckPossible = bool(self.hiddenCards(LOCATION.deck))
        if justCheck:
            return bool(handVictims or deckPossible)

        monster = None
        if handVictims:
            monster = self.morph(handVictims[0], key)
        if monster is None:
            # Deck route: morph deck card -> deck top -> normal-looking draw
            planted = self.provideOnDeckTop(key)
            if planted is None:
                return False
            drawn = yield game.y_drawCard(side, 1)
            if not drawn or drawn[0] is not planted:
                return False
            monster = planted
            yield WaitForSeconds(1)

        ok = yield bot.y_playerlikeNormalSummon(monster, costNormalSummonChance=False)
        if ok:
            rec = getattr(bot, "_recordSummon", None)
            if rec:
                rec(getattr(monster, "cardKey", None))   # track for last-turn avoidance
            yield WaitForSeconds(2)
        return ok

    def y_signatureSummon(self, justCheck):
        """Morph a hidden hand card into a signature monster, then
        special-summon it FROM HAND — the opponent sees a normal hand card
        being played."""
        bot = self.bot
        game = bot.game

        if justCheck:
            keys = [k for k in (bot.signatureMonstersPool or []) if self.canCreateMore(k)]
            return any(self._morphCandidatesInHand([k]) for k in keys)

        key = self.pickCreatableFromPool(bot.signatureMonstersPool)
        if not key:
            return False
        victims = self._morphCandidatesInHand([key])
        if not victims:
            return False
        monster = self.morph(victims[0], key)
        if monster is None:
            return False
        yield WaitForSeconds(random.uniform(1, 2))
        ok = yield game.y_specialSummon(monster)
        if ok:
            bot.signatureOnField = True
            AI_MSG("[supply] signature from hand:", key)
        return ok
