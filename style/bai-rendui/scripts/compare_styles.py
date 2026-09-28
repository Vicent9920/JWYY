# -*- coding: utf-8 -*-
"""两篇文本的写作风格一致性对比（文学维度，非 AIGC 指标）
用途；判断「炉火」与「百人队」是否同一风格 → 决定是否需分开提炼 Skill
"""
import re, sys, math, collections

CN = re.compile(r'[\u4e00-\u9fff]')
def cc(s): return len(CN.findall(s))

SENT = re.compile(r'[^。！？…\n]+[。！？…]?')
def sents(t):
    out = []
    for p in t.split('\n'):
        for m in SENT.finditer(p):
            s = m.group().strip()
            if cc(s): out.append(s)
    return out

# ---------- 词表 ----------
FINAL_PART = ('吧','罢','呢','啊','呀','哪','嘛','么','咧','哩','呐','哦','喽','哉')
FINAL_MULTI = ('罢了','而已','就是了','得了','不成','才是','便是')
COLLOQ = ('其实','反正','干脆','索性','偏偏','到底','好歹','横竖','左右','倒是',
          '敢是','端的','偏生','何苦','管他','不消','省得','免得','总不能','难不成','爱怎么')
INTERJ = ('咳','嗐','咦','啐','哎','嗯','唔','嘿','欸','喏')
SIMILE = ('就像','好像','像是','仿佛','好比','似的','如同','一如','恍如','恰似','宛如')
CONNECT = ('因此','所以','然而','但是','而且','并且','于是','至于','总之','况且','何况',
           '即使','即便','无论','尽管','不仅','而是','因而','从而')
CLASSICAL = ('之','其','乃','则','矣','焉','者','where')[:7]   # 文言虚词
PHYSIO = ('手抖','发抖','抖','喉头','眼圈','后背','后颈','汗','掐','攥','膝盖','腿','脸',
          '牙关','脊背','头皮','喘','眼睛','嗓子','胸口','指尖','脖子')  # 生理/体态外化
PSYCH = ('觉得','感到','难过','愤怒','生气','高兴','害怕','恐惧','担心','焦虑','伤心','开心')
TIMESTAMP = ('次日','翌日','三天后','第二天','隔日','数日后','半个月后','一个月后','年后')
NATTIME = ('晌午','日头','傍晚','夜里','早晨','半夜','清晨','早上','午后','天黑','天快黑','黄昏')
MEASURE = ('斤','两','里','尺','寸','个','只','头','匹','把','壶','碗','队伍','门','支','座','条','层','道')

def dens(body, total, words):
    return 1000 * sum(body.count(w) for w in words) / total

def measure(path, label):
    t = open(path, encoding='utf-8').read()
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    paras = [l for l in lines if not l.startswith('#')]
    tx = '\n'.join(paras)
    body = tx.replace('\n', '')
    total = cc(body) or 1
    SI = sents(tx)
    sl = [cc(s) for s in SI]
    n = len(SI) or 1
    mu = sum(sl) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in sl) / n)
    dlg = re.findall(r'“([^”]*)”', tx)
    dlgc = sum(cc(x) for x in dlg)
    pl = [cc(p) for p in paras]
    pmu = sum(pl) / len(pl)
    psd = math.sqrt(sum((x - pmu) ** 2 for x in pl) / len(pl))

    fin = []
    for s in SI:
        core = s.rstrip('。！？…')
        for w in FINAL_MULTI:
            if core.endswith(w): fin.append(w); break
        else:
            if core and core[-1] in FINAL_PART: fin.append(core[-1])

    dlg_sent_len = [cc(s) for s in SI if '“' in s]

    F = collections.OrderedDict()
    # --- A 人称与视角 ---
    F['A 我‰'] = 1000 * body.count('我') / total
    F['A 他‰'] = 1000 * body.count('他') / total
    F['A 你‰'] = 1000 * body.count('你') / total
    F['A 第一人称句占比%'] = 100 * sum(1 for s in SI if '我' in s) / n
    # --- B 句法节奏 ---
    F['B 句均长'] = mu
    F['B 句中位'] = sorted(sl)[n // 2]
    F['B 句长变异系数'] = sd / mu if mu else 0
    F['B 短句≤10占比%'] = 100 * sum(1 for x in sl if x <= 10) / n
    F['B 长句≥40占比%'] = 100 * sum(1 for x in sl if x >= 40) / n
    F['B ≥3逗号句占比%'] = 100 * sum(1 for x in SI if s.count('，') >= 3) / n
    F['B 逗号比句号'] = body.count('，') / max(1, body.count('。'))
    # --- C 段落 ---
    F['C 段均长'] = pmu
    F['C 段中位'] = sorted(pl)[len(pl) // 2]
    F['C 段长变异系数'] = psd / pmu if pmu else 0
    F['C 单句段占比%'] = 100 * sum(1 for p in paras if len(sents(p)) == 1) / len(paras)
    F['C 含引号段占比%'] = 100 * sum(1 for p in paras if '“' in p) / len(paras)
    F['C 段内逗号均'] = sum(p.count('，') for p in paras) / len(paras)
    # --- D 标点 ---
    F['D 顿号‰'] = 1000 * body.count('、') / total
    F['D 分号‰'] = 1000 * body.count('；') / total
    F['D 破折号‰'] = 1000 * body.count('——') / total
    F['D 省略号‰'] = 1000 * body.count('…') / total
    F['D 感叹号‰'] = 1000 * body.count('！') / total
    F['D 问号‰'] = 1000 * body.count('？') / total
    F['D 引号组/千字'] = 1000 * len(dlg) / total
    # --- E 词汇层 ---
    F['E 句末语气助词‰'] = 1000 * len(fin) / total
    F['E 口语标记词‰'] = dens(body, total, COLLOQ)
    F['E 叹词‰'] = dens(body, total, INTERJ)
    F['E 明喻‰'] = dens(body, total, SIMILE)
    F['E 逻辑连接‰'] = dens(body, total, CONNECT)
    F['E 文言虚词‰'] = dens(body, total, CLASSICAL)
    F['E "也"‰'] = 1000 * body.count('也') / total
    # --- F 具体性 ---
    F['F 数字密度‰'] = 1000 * (len(re.findall(r'\d', body)) + len(re.findall(r'[一二三四五六七八九十百千万两]', body))) / total
    F['F 量词密度‰'] = dens(body, total, MEASURE)
    # --- G 情绪外化 ---
    F['G 生理体态‰'] = dens(body, total, PHYSIO)
    F['G 心理直陈‰'] = dens(body, total, PSYCH)
    F['G 外化/直陈比'] = (dens(body, total, PHYSIO) / dens(body, total, PSYCH)) if dens(body, total, PSYCH) else float('inf')
    # --- H 时间 ---
    F['H 时间戳‰'] = dens(body, total, TIMESTAMP)
    F['H 自然时间‰'] = dens(body, total, NATTIME)
    # --- I 对话形态 ---
    F['I 对话占比%'] = 100 * dlgc / total
    F['I 含对话句均长'] = (sum(dlg_sent_len) / len(dlg_sent_len)) if dlg_sent_len else 0
    F['I 平均对话长度'] = (dlgc / len(dlg)) if dlg else 0

    F['__meta__'] = (label, total, len(paras), n)
    return F

def table(files):
    Fs = [measure(p, l) for p, l in files]
    lbl = [F['__meta__'][0] for F in Fs]
    print('=' * 108)
    for F in Fs:
        l, tot, np_, ns = F['__meta__']
        print('  %-22s  汉字 %4d  段 %2d  句 %3d' % (l, tot, np_, ns))
    print('=' * 108)
    print('%-18s %10s %10s | %9s %9s' % ('维度', lbl[0][:9], lbl[1][:9], '差值', '偏差%'))
    print('-' * 108)
    keys = [k for k in Fs[0] if k != '__meta__']
    big = []
    for k in keys:
        v = [F[k] for F in Fs]
        d = v[0] - v[1]
        base = (abs(v[0]) + abs(v[1])) / 2
        dev = 100 * d / base if base else 0
        mark = '  <<< 差异大' if abs(dev) > 50 else ('  < 差异中' if abs(dev) > 25 else '')
        if abs(dev) > 50: big.append(k)
        print('%-18s %10.2f %10.2f | %9.2f %8.0f%%%s' % (k, v[0], v[1], d, dev, mark))
    print('-' * 108)
    print('差异 >50%% 的维度：%d 项' % len(big))
    for k in big: print('   -', k)
    return Fs, big

if __name__ == '__main__':
    import os
    os.chdir(r'D:\tmp\aigc_optimized')
    print('\n########## 对照 1：改写前的原始稿 ##########\n')
    table([(r'D:\tmp\aigc_opt\seg0_stove.txt', '炉火(原始)'),
           (r'D:\tmp\aigc_opt\seg1_flagged.txt', '百人队(原始)')])
    print('\n\n########## 对照 2：当前的优化稿 ##########\n')
    table([('炉火_优化版.txt', '炉火(优化版)'),
           ('百人队_优化版.txt', '百人队(优化版)')])
