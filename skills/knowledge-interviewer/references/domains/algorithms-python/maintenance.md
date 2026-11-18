# 算法域维护

新增/修改时同步 catalog.json、map.md、正文唯一二级标题、knowledge-map.md、题库、复习卡和评测定义。稳定ID不复用；前置必须可定位且无环。来源核对日期只对实际打开的页面有效，不把链接存在写成逐题认证。

```bash
python3 scripts/check_system.py
python3 -m unittest discover -s handbook/algorithms-python/examples -p 'test_*.py' -v
python3 -m unittest discover -s skills/knowledge-interviewer/scripts -p 'test_*.py'
python3 skills/knowledge-interviewer/scripts/check_learning_privacy.py
```

代码改动增加能检出错误策略的反例/小规模对拍，不用大样本耗时当正确性证明。平台语言版本/输入输出先核实，不假设每题都支持同一解释器。evals中的合成行为案例未执行就保持not_run，不编造grades或借旧域成绩。不要改写任何个人进度、错题或偏好。
