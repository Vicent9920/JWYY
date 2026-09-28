---
inclusion: always
---

# 一致性

权威顺序：`bible/` 与 `outline/volume-01.md`、`outline/volume-structure.md` 高于 `books/` 里的生成稿。

## 写一章之前，先读

1. `bible/文风.md` 与 `.cursor/rules/style.mdc`
2. 本章锁点（`outline/volume-01.md` 或对应 `outline/chapters/`）
3. `bible/timeline.md` 里不晚于本章的事件
4. `bible/foreshadowing.md` 里状态不是「已回收」的条目，禁止提前引爆
5. 本章会上场的人物卡：`bible/02_人物卡_v1.md`，以及 `books/建文演义/story/roles/` 里对应的卡
6. `books/建文演义/story/book_rules.md`

缺锁点的幕，不得连续开写。c01 除外，它的锁点已经在 `outline/volume-01.md`。

## 写完一章之后，必须回写

1. 统计标题之后的纯汉字。卷一常规章不少于 4000，c01 不少于 4500。不够就继续改，不得标成稿。
2. `bible/timeline.md` 把该事件从「计划」改为「已写」，或在写后追加区记一行。
3. `bible/foreshadowing.md` 更新状态：待埋 / 已埋 / 已强化 / 已回收。
4. 人物若换了立场、位置、知道的事，改对应角色卡的「当前现状」。
5. 跑 `python style/bai-rendui/scripts/bai_style_check.py`。表一、表二都过，才算这一章可留。

## 写的时候随时核对

- 火器不碾压。神机营未成军之前，不要写成已经能打仗。
- 金手指是知道，不是会造，也不是记忆衰减。
- 秘书室不得代六部行事。1398 年用锦衣卫，不写东厂。
- 不写程砚。不写方孝孺诛十族。不写朱棣死在卷四。
- 卷一四幕职责不要串：c01 只到登基回宫，不建室，不绑姚，不削藩。
