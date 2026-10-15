# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def update_item(self, name, sell_in, quality):
        item = Item(name, sell_in, quality)
        GildedRose([item]).update_quality()
        return item

    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_standard_item_decreases_quality_and_sell_in(self):
        item = self.update_item("+5 Dexterity Vest", 5, 10)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(9, item.quality)

    def test_standard_item_degrades_twice_after_expiration(self):
        item = self.update_item("+5 Dexterity Vest", 0, 10)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(8, item.quality)

    def test_standard_item_quality_never_goes_below_zero(self):
        item = self.update_item("+5 Dexterity Vest", 5, 0)
        self.assertEqual(0, item.quality)

    def test_standard_item_quality_reaches_zero_after_expiration(self):
        item = self.update_item("+5 Dexterity Vest", 0, 1)
        self.assertEqual(0, item.quality)

    # Aged Brie
    def test_aged_brie_increases_quality(self):
        item = self.update_item("Aged Brie", 5, 10)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(11, item.quality)

    def test_aged_brie_increases_quality_twice_after_expiration(self):
        item = self.update_item("Aged Brie", 0, 10)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(12, item.quality)

    def test_aged_brie_quality_never_exceeds_fifty(self):
        item = self.update_item("Aged Brie", 5, 49)
        self.assertEqual(50, item.quality)

    def test_aged_brie_quality_at_maximum_quality_stays_at_fifty(self):
        item = self.update_item("Aged Brie", 5, 50)
        self.assertEqual(50, item.quality)

    # Sulfuras
    def test_sulfuras_never_changes(self):
        item = self.update_item("Sulfuras, Hand of Ragnaros", 5, 80)
        self.assertEqual(5, item.sell_in)
        self.assertEqual(80, item.quality)

    def test_sulfuras_never_changes_after_expiration(self):
        item = self.update_item("Sulfuras, Hand of Ragnaros", -1, 80)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(80, item.quality)

    # Backstage passes
    def test_backstage_pass_increases_by_one_when_more_than_ten_days_remain(self):
        item = self.update_item("Backstage passes to a TAFKAL80ETC concert", 11, 20)
        self.assertEqual(10, item.sell_in)
        self.assertEqual(21, item.quality)

    def test_backstage_pass_increases_by_two_at_ten_days(self):
        item = self.update_item("Backstage passes to a TAFKAL80ETC concert", 10, 20)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(22, item.quality)

    def test_backstage_pass_increases_by_three_at_five_days(self):
        item = self.update_item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(23, item.quality)

    def test_backstage_pass_drops_to_zero_on_concert_day(self):
        item = self.update_item("Backstage passes to a TAFKAL80ETC concert", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_backstage_pass_drops_to_zero_after_concert_day(self):
        item = self.update_item("Backstage passes to a TAFKAL80ETC concert", -1, 20)
        self.assertEqual(-2, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_backstage_pass_quality_never_exceeds_fifty(self):
        item = self.update_item("Backstage passes to a TAFKAL80ETC concert", 5, 50)
        self.assertEqual(50, item.quality)

    # Conjured: nouvelle fonctionnalité à implémenter
    def test_conjured_item_degrades_twice_as_fast(self):
        item = self.update_item("Conjured Mana Cake", 5, 10)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(8, item.quality)

    def test_conjured_item_degrades_four_times_after_expiration(self):
        item = self.update_item("Conjured Mana Cake", 0, 10)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(6, item.quality)

    def test_conjured_item_quality_never_goes_below_zero(self):
        item = self.update_item("Conjured Mana Cake", 5, 1)
        self.assertEqual(0, item.quality)

    def test_conjured_item_at_zero_quality_stays_at_zero(self):
        item = self.update_item("Conjured Mana Cake", 5, 0)
        self.assertEqual(0, item.quality)


if __name__ == "__main__":
    unittest.main()
