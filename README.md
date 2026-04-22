# I N Q U I S I T O R

**A personal movie content warning system.**
**一个私人电影内容预警系统。**

> 「我岂没有吩咐你吗？你当刚强壮胆！不要惧怕，也不要惊惶；因为你无论往哪里去，耶和华你的神必与你同在。」── 约书亚记 1:9

---

## Why / 为什么

I never watch horror. It makes my heart physically hurt.

But I didn't expect to feel it during the opening of a Bond film.

*No Time to Die.* A white mask, flashing across the screen. Suffocating silence. A figure walking slowly through snow. Ten minutes in — chest tight, heart pounding. In a movie I thought was an action film.

**I'm done.**

Done with jump scares hiding inside thrillers. Done with dread scattered across shows that aren't supposed to be scary. I don't want to open *Doctor Who* for some family fun and walk straight into the Weeping Angels — something that stayed with me for years. If I'd known, I would've just watched *Resident Evil* instead. Scarier on paper — but at least I'd know what I was getting into. One sleep and I'd forget.

The problem was never horror itself. The problem was **not knowing**.

我从来不看恐怖片。会让我心脏不舒服。

可没想到会在007无暇赴死开头体验到如此令人不安的元素。一闪而过的白面具，压抑的氛围，雪地里慢慢走来的人影。我以为这是一部动作片。结果前十分钟胸口就发紧了。

**我受够了。**

我受够了 jump scare 藏在惊悚片里。受够了意味深长的恐吓散落在各种不是恐怖片的片型里。我不想再打开神秘博士看个合家欢结果看到天使石像——这种令我记了半辈子的吓人东西。如果早知道如此，我不如看生化危机——更吓人，但我知道。睡一觉就忘。

问题从来不是恐怖片本身。问题是**不知道**。

---

## What / 是什么

INQUISITOR is a personal movie content warning tool powered by AI. You tell it a movie name, it tells you how scared you'll be — based on YOUR taste, not some generic rating system.

It's not a product. It's a tool I built for myself. If you want to use it, configure your own API key and calibration table. If you don't know how — figure it out.

INQUISITOR 是一个 AI 驱动的私人电影内容预警工具。你给它电影名，它告诉你——以你自己的标准——你会不会害怕。

这不是产品，是我给自己造的工具。想用就自己配。不会的自己学。

---

## The hard part / 难点：教 AI 理解你怕什么

### v0: Keywords / 关键词

I listed trigger words. "Masks." "Jump scares." "Cult." "Dark corridors."

The AI matched them like a checklist. *Taxi Driver* got 3 stars. *Raging Bull* got 4. I'm not scared of either.

**Keywords are labels. Labels are bias.**

我列了一堆关键词。"面具"、"jump scare"、"邪教"、"黑暗走廊"。AI 像查清单一样匹配它们。出租车司机给了三星。愤怒的公牛给了四星。这两部我完全不怕。

**关键词是贴标签。标签是偏见的源头。**

### v1–v2: Rules and examples / 规则与案例

I added rules: "Judge by technique, not violence level." I added examples: "The opening of *No Time to Die* = severe."

Better. But the AI over-anchored to my examples and over-analyzed everything.

我加了规则："按手法判断，不按暴力程度。"加了案例："007开头 = 严重。"

好了一些。但 AI 偏锚到了案例上，过度分析一切。

### v3: Director's intent / 导演意图

I told the AI: "Is the director trying to scare the audience?"

This helped — but it still flagged *Westworld* as severe. It saw "cult" and "oppressive atmosphere" and panicked. Even though Westworld's eeriness is worldbuilding, not horror.

我告诉 AI："导演是在试图吓观众吗？"

有进步。但它还是把西部世界标成严重——因为它看到了"邪教"、"压抑氛围"就升级了。哪怕西部世界的诡异是科幻叙事，不是恐怖手法。

### v4: Delete everything. Give data. / 删掉一切，给数据

I deleted all keywords. All rules. All frameworks.

I kept only one thing: **a calibration table — real movies I've watched, with my real reactions.**

The AI's job became: "Which movie in the table is this most similar to?"

**It worked.**

我删掉了所有关键词、规则、框架。只留了一样东西：**校准表——我真实看过的电影，和我真实的反应。**

AI 的任务变成了："这部电影最像校准表里的哪一部？"

**终于准了。**

### v5: Data + reasoning / 数据 + 思考指引

A pure lookup table wasn't enough. The AI still needed to know *how* to use the data.

One instruction solved it: "Find the closest match. Ask if the director is trying to scare you. When in doubt, rate lower, not higher."

Data is the truth. But even truth needs a method to be read correctly.

纯查表还不够。AI 需要知道**怎么用**这张表。

一条指引解决了："先找最像的参照。再问导演是不是在吓你。拿不准的时候，往低给，不往高给。"

数据是真理。但真理也需要方法才能被正确解读。

---

## Rating / 分级

| Stars | Meaning | 含义 |
|-------|---------|------|
| ★ | Not scared at all | 完全不怕 |
| ★★ | Suspenseful, thrilling but enjoyable | 有氛围，刺激但想看 |
| ★★★ | A bit scared but can finish | 有点害怕但能看完 |
| ★★★★ | Many scary moments, need to fast-forward | 很多地方害怕，得快进 |
| ★★★★★ | Don't watch | 别看 |

This is not a rating board. There is only one axis: **how uncomfortable will I be?**

*Tom and Jerry* and *Taxi Driver* are both ★. Because I'm not scared of either.

这不是分级协会。只有一个维度：**我会不会不舒服？** 猫和老鼠跟出租车司机都是一星。因为我都不怕。

---

## Setup / 安装

Python 3.12+ required. Get an API key from [OpenRouter](https://openrouter.ai), [DeepSeek](https://platform.deepseek.com), or run a local model with [Ollama](https://ollama.ai).

```bash
git clone https://github.com/magnusy01/inquisitor.git
cd inquisitor
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cp taste_template.json taste.json
```

Edit `.env` with your API key. Edit `taste.json` with your own movies. Then:

```bash
python inquisitor_app.py
```

If you can't figure this out, this tool is not for you.

如果你连这都搞不定，这个工具不适合你。

---

## Build your calibration table / 建造你的校准表

1. Think of movies you've watched. 想想你看过的电影。
2. Rate each one: how scared were you? ★ to ★★★★★ 给每部评星：你有多害怕？
3. Put them in `taste.json`. 填进校准表。
4. Test on a movie you've seen — does the AI agree? 测试——AI 同意你的评分吗？
5. Wrong? Add that movie at the correct level. 不对？加到正确的星级。
6. Repeat. More data = more accurate. 重复。数据越多越准。

**Your taste is your data. Your data is your tool.**

**你的品味就是你的数据。你的数据就是你的工具。**

---

## What I learned / 我学到了什么

Don't teach AI rules. Give it your experience.

Keywords are labels — someone else's categories forced onto your feelings. Your body knows what scares you better than any checklist.

Every movie you add is a data point. Every data point makes the system more *you*. No prompt engineering trick beats real data from real experience.

不要教 AI 规则。给它你的体验。

关键词是标签——是别人的分类强加在你的感受上。你的身体比任何清单都更知道什么让你害怕。

校准表里的每一部电影都是一个数据点。每一个数据点都让系统更像你。再精巧的提示词工程也比不上真实体验的真实数据。

---

*Built across four nights. From zero Python to first GitHub release.*

*四个夜晚，从零到发布。*

*Authored by magnusy · 2026*
