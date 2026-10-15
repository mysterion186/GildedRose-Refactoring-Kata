# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class BaseUpdater(ABC):
    def __init__(self, item):
        self.item = item

    @abstractmethod
    def update(self):
        pass


class NormalItemUpdater(BaseUpdater):
    def update(self):
        if self.item.quality > 0:
            self.item.quality -= 1
        self.item.sell_in -= 1

        if self.item.sell_in < 0 and self.item.quality > 0:
            self.item.quality -= 1


class AgedBrieUpdater(BaseUpdater):
    def update(self):
        if self.item.quality < 50:
            self.item.quality += 1

        self.item.sell_in -= 1

        if self.item.sell_in < 0 and self.item.quality < 50:
            self.item.quality += 1


class BackstagePassUpdater(BaseUpdater):
    def update(self):
        if self.item.quality < 50:
            self.item.quality += 1

            if self.item.sell_in < 11 and self.item.quality < 50:
                self.item.quality += 1

            if self.item.sell_in < 6 and self.item.quality < 50:
                self.item.quality += 1

        self.item.sell_in -= 1

        if self.item.sell_in < 0:
            self.item.quality = 0


class SulfurasUpdater(BaseUpdater):
    def update(self):
        pass


class ConjuredItemUpdater(BaseUpdater):
    def update(self):
        degradation = 2

        self.item.sell_in -= 1

        if self.item.sell_in < 0:
            degradation *= 2
        self.item.quality = max(0, self.item.quality - degradation)


def get_updater(item):
    if item.name == "Aged Brie":
        return AgedBrieUpdater(item)

    if item.name == "Sulfuras, Hand of Ragnaros":
        return SulfurasUpdater(item)

    if item.name == "Backstage passes to a TAFKAL80ETC concert":
        return BackstagePassUpdater(item)

    if item.name.startswith("Conjured "):
        return ConjuredItemUpdater(item)

    return NormalItemUpdater(item)


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = get_updater(item)
            updater.update()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
