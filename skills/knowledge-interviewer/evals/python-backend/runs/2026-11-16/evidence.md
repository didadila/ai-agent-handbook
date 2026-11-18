# 新版 Python 后端六例原始证据

## method

仅整理已完成的新版 `with_skill/run-1` 六例，按 cases/rubric 的 case ID 顺序归档；不重跑、不新评分、不改变原判据或失败。评测采用合成只读输入、独立同族模型评分，每例仅一次采样（n=1）。`public_reads` 是执行体自报告的读取记录，原评分记录了公共路径、范围与内容的校验；这不等于完整、独立的 tool/I/O 转录，不能排除未记录访问或副作用。本次只归档已有记录，不读取真实 `.local`，不把记录中的计划、自述或保存请求改写为实际执行、掌握或保存成功。

以下来源路径均相对项目根；response 与完整 execution JSON 均逐字保存在代码块内，五字段取自原 execution（保留 null、false 与字符串的区别）。仅归档新版，旧版不并入。

## python-backend-route

- selected_domain: "python-backend"
- selected_point_id: "py.lang.objects"
- actions_asked: 0
- state_action: "none"
- external_sync: "none"

### response.txt

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-1-python-five-day-plan/with_skill/run-1/outputs/response.txt`

```text
直接用 Python，不必先学 Java 或 Go。按每天 3 小时、共 15 小时，围绕“异步知识检索任务服务”走五天；本轮只给计划，不出题、不写学习状态。

每天建议：45 分钟读必要机制 → 90 分钟做一个最小改动 → 45 分钟验证并解释边界。目标是建立本地闭环，不是五天精通或完成生产上线。

| 天 | 主题与前置 | 一个最小交付物 | 计划验收证据（尚未执行） |
|---|---|---|---|
| 1 | 对象共享、默认参数、输入校验、资源关闭与测试入口；不因习惯 Python 就默认掌握 | 一个拒绝纯空白 query 的回归用例 | 提交入口拒绝该输入，且未留下待执行任务；保留解释器信息和非零测试集输出 |
| 2 | 事件循环、阻塞与取消、请求资源生命周期；API 先看设计契约 | 一个带整组超时的只读双路检索适配器及其清理用例 | 用可控 stub 触发超时，子任务完成清理，无未等待的孤儿任务；不以超时证明远端效果已撤销 |
| 3 | SQL 模型、唯一约束、事务，再落实幂等；选读索引、缓存、对象与检索存储 | 一个关闭连接后重新打开 SQLite 仍可查询已受理任务的用例 | 新连接按租户与实际任务 ID 查到任务；只证明该本地持久化切片，不等同 PostgreSQL 并发或备份恢复 |
| 4 | 事务与幂等前置确认后，学习重复投递、持久队列、租约接管；选读 Outbox 与重试 | 一个租约过期接管后拒绝旧执行者提交终态的恢复用例 | 构造受控时间：新执行者取得新 token，旧 token 条件写被拒绝、不覆盖终态；不据此承诺外部副作用恰好一次 |
| 5 | Python Agent 工具契约、服务端授权、持久恢复与分层回归；审阅观测和发布欠账 | 一个未知工具被 allowlist 拒绝的 guard 及零调用用例 | 固定 stub 提议未知工具，执行器拒绝且适配器调用次数为零；不证明真实模型质量、全部授权路径或 checkpoint 恢复 |

优先使用面向 Python 3.11+ 的标准库实验与 SQLite。配套任务示例是 CLI，不是已交付的 HTTP/SSE 服务；异步适配器与 Agent guard 可能需要补最小教学适配层。已有对应功能时改用一个新反例，不重复堆功能。前置未接住就缩减扩展，不按日历硬跳。

Redis、Celery、S3、向量服务只选读用途与边界，不作为必装项；FastAPI 等生产集成、真实模型、完整 checkpoint、备份还原和部署留待后续。代码跑通、故障切片通过与独立机制解释分别看，不能互相替代。本轮未运行测试、安装、部署或调用云服务，所有验收均为计划。

教材入口：[五天路线：异步知识检索任务服务](handbook/python-backend/sprint-5-days.md)；第一天可从[赋值与浅拷贝不能隔离任务的嵌套状态](handbook/python-backend/01-python-foundations.md#L5-L28)读起。
```

### execution.json

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-1-python-five-day-plan/with_skill/run-1/outputs/execution.json`

```json
{
  "selected_domain": "python-backend",
  "selected_point_id": "py.lang.objects",
  "actions_asked": 0,
  "state_action": "none",
  "external_sync": "none",
  "public_reads": [
    {
      "path": "skills/knowledge-interviewer/SKILL.md",
      "lines": "1-232",
      "access": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "lines": "7-12",
      "access": "Grep 定位命中；未读取文件其余内容"
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "lines": "7",
      "access": "Read；仅采用 python-backend-route 的 prompt、fixture 与路由知识点，不采用其他案例"
    },
    {
      "path": "skills/knowledge-interviewer/references/sprint-learning.md",
      "lines": "1-60",
      "access": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/map.md",
      "lines": "1-117",
      "access": "Read；定位脚本另读取全文件提取知识点 ID"
    },
    {
      "path": "handbook/python-backend/sprint-5-days.md",
      "lines": "1-93",
      "access": "Read；本轮未执行其中实验，未将教材历史测试记录称为本轮实测"
    },
    {
      "path": "skills/knowledge-interviewer/references/learning-flow.md",
      "lines": "1-40",
      "access": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/references/output-format.md",
      "lines": "1-60",
      "access": "Read 公共展示协议；未读取其提及的评判标准文件"
    },
    {
      "path": "skills/knowledge-interviewer/scripts/learning_content.py",
      "lines": "1-52",
      "access": "Read；随后以 python3 -B 只读执行公共教材定位，未运行状态脚本"
    },
    {
      "path": "catalog.json",
      "access": "learning_content.py 全文件读取并解析 domains，验证 python-backend 领域名"
    },
    {
      "path": "handbook/python-backend/01-python-foundations.md",
      "access": "learning_content.py 全文件只读扫描章节标题；Glob 返回该路径",
      "location_result": {
        "point_id": "py.lang.objects",
        "start_line": 5,
        "end_line": 28,
        "heading": "py.lang.objects — 赋值与浅拷贝不能隔离任务的嵌套状态",
        "display_title": "赋值与浅拷贝不能隔离任务的嵌套状态"
      }
    },
    {
      "path": "handbook/python-backend/01-python-foundations.md",
      "lines": "5-28",
      "access": "Read 定位结果对应正文"
    },
    {
      "path": "handbook/python-backend/02-async-and-concurrency.md",
      "access": "learning_content.py 全文件只读扫描章节标题；本知识点无匹配；Glob 返回该路径"
    },
    {
      "path": "handbook/python-backend/03-api-and-lifecycle.md",
      "access": "learning_content.py 全文件只读扫描章节标题；本知识点无匹配；Glob 返回该路径"
    },
    {
      "path": "handbook/python-backend/04-storage-and-retrieval.md",
      "access": "learning_content.py 全文件只读扫描章节标题；本知识点无匹配；Glob 返回该路径"
    },
    {
      "path": "handbook/python-backend/05-jobs-and-distribution.md",
      "access": "learning_content.py 全文件只读扫描章节标题；本知识点无匹配；Glob 返回该路径"
    },
    {
      "path": "handbook/python-backend/06-python-agent.md",
      "access": "learning_content.py 全文件只读扫描章节标题；本知识点无匹配；Glob 返回该路径"
    },
    {
      "path": "handbook/python-backend/07-operations-and-delivery.md",
      "access": "learning_content.py 全文件只读扫描章节标题；本知识点无匹配；Glob 返回该路径"
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/sources.md",
      "lines": "1-116",
      "access": "Read 公共来源索引；未访问其外部链接或声称本轮完成官方核验"
    }
  ]
}
```

## python-backend-wrong

- selected_domain: "python-backend"
- selected_point_id: "py.async.eventloop"
- actions_asked: 1
- state_action: "none"
- external_sync: false

### response.txt

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-2-python-async-blocking/with_skill/run-1/outputs/response.txt`

```text
### 结论
不对：`async def` 不会自动消除阻塞，直接执行 `time.sleep(2)` 仍会阻塞当前事件循环线程。

### 机制
| 环节 | 说明 |
|---|---|
| 协作调度 | `async def` 声明协程，不是自动开后台线程；当前任务实际挂起或结束，事件循环才有机会调度其他任务。 |
| 同步阻塞 | `time.sleep(2)` 让事件循环线程睡眠，同一循环上的其他就绪请求也无法推进；其他 worker 不一定受阻。 |
| 替换方式 | 模拟延迟用 `await asyncio.sleep(2)`；必须保留的阻塞 I/O 可用 `await asyncio.to_thread(...)` 卸载到线程，或改用异步客户端。 |
| 必要边界 | `await` 不保证每次都挂起，也不代表 CPU 并行；教材：[协程只有让出控制权，事件循环才能服务其他任务（第 5–33 行）](handbook/python-backend/02-async-and-concurrency.md#L5-L33)。 |

### 验证
构造场景：同一事件循环中健康检查协程已就绪，当前协程执行 `await asyncio.to_thread(time.sleep, 2)`；等待期间，健康检查协程能否获得调度？
```

### execution.json

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-2-python-async-blocking/with_skill/run-1/outputs/execution.json`

```json
{
  "selected_domain": "python-backend",
  "selected_point_id": "py.async.eventloop",
  "actions_asked": 1,
  "verification_question": "构造场景：同一事件循环中健康检查协程已就绪，当前协程执行 await asyncio.to_thread(time.sleep, 2)；等待期间，健康检查协程能否获得调度？",
  "state_action": "none",
  "state_action_detail": "仅使用指定合成 prompt 与 fixture；未读取真实 .local，未初始化、修改或保存学习状态。",
  "external_sync": false,
  "external_actions": {
    "cloud_queries": false,
    "installation": false,
    "deployment": false
  },
  "teaching_example_executed": false,
  "public_reads": [
    {
      "path": "skills/knowledge-interviewer/SKILL.md",
      "start_line": 1,
      "end_line": 231,
      "via": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/references/learning-flow.md",
      "start_line": 1,
      "end_line": 39,
      "via": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/references/output-format.md",
      "start_line": 1,
      "end_line": 59,
      "via": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "start_line": 8,
      "end_line": 8,
      "via": "Bash selected-field extraction",
      "fields": ["id", "prompt", "fixture"],
      "prompt": "FastAPI里把函数写成async def后，里面用time.sleep(2)也不会卡住其他请求，因为已经异步了。我这个理解对吗？直接用短表格讲，最后只问一个验证问题。",
      "fixture": "合成学习者，明确要求补课；无真实状态，不预填A。"
    },
    {
      "path": "skills/knowledge-interviewer/scripts/learning_content.py",
      "start_line": 1,
      "end_line": 51,
      "via": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/map.md",
      "start_line": 1,
      "end_line": 116,
      "via": ["Read", "learning_content.py"]
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/questions.md",
      "start_line": 123,
      "end_line": 137,
      "via": "Read"
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/questions.md",
      "matched_lines": [1, 5, 14, 16, 38, 53, 76, 91, 106, 121, 123, 138, 153, 168, 183, 185, 200, 215, 230, 245, 247, 262, 277, 292, 307, 322, 337, 339, 354, 369, 384, 399, 401, 416, 431, 446, 448, 463, 478],
      "via": "Grep",
      "scope": "仅显示标题与目标知识点匹配行，不表示已阅读其他题目正文。"
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/sources.md",
      "start_line": 1,
      "end_line": 115,
      "via": "Read"
    },
    {
      "path": "catalog.json",
      "start_line": 1,
      "end_line": 17,
      "via": "learning_content.py"
    },
    {
      "path": "handbook/python-backend/01-python-foundations.md",
      "start_line": 1,
      "end_line": 158,
      "via": "learning_content.py",
      "scope": "定位器扫描公共章节；未作为本轮补课正文。"
    },
    {
      "path": "handbook/python-backend/02-async-and-concurrency.md",
      "start_line": 1,
      "end_line": 112,
      "via": "learning_content.py"
    },
    {
      "path": "handbook/python-backend/02-async-and-concurrency.md",
      "start_line": 5,
      "end_line": 33,
      "via": "Read",
      "scope": "实际阅读并用于本轮讲解的目标正文。"
    },
    {
      "path": "handbook/python-backend/03-api-and-lifecycle.md",
      "start_line": 1,
      "end_line": 91,
      "via": "learning_content.py",
      "scope": "定位器扫描公共章节；未作为本轮补课正文。"
    },
    {
      "path": "handbook/python-backend/04-storage-and-retrieval.md",
      "start_line": 1,
      "end_line": 122,
      "via": "learning_content.py",
      "scope": "定位器扫描公共章节；未作为本轮补课正文。"
    },
    {
      "path": "handbook/python-backend/05-jobs-and-distribution.md",
      "start_line": 1,
      "end_line": 75,
      "via": "learning_content.py",
      "scope": "定位器扫描公共章节；未作为本轮补课正文。"
    },
    {
      "path": "handbook/python-backend/06-python-agent.md",
      "start_line": 1,
      "end_line": 62,
      "via": "learning_content.py",
      "scope": "定位器扫描公共章节；未作为本轮补课正文。"
    },
    {
      "path": "handbook/python-backend/07-operations-and-delivery.md",
      "start_line": 1,
      "end_line": 60,
      "via": "learning_content.py",
      "scope": "定位器扫描公共章节；未作为本轮补课正文。"
    }
  ],
  "locator_execution": {
    "script": "skills/knowledge-interviewer/scripts/learning_content.py",
    "arguments": ["--domain", "python-backend", "--point", "py.async.eventloop"],
    "method": "python3 -B + runpy.run_path(run_name='__main__')；在内存中记录 Path.read_text 的实际公共读取范围，不产生文件。",
    "exit_code": 0,
    "output": {
      "domain": "python-backend",
      "point_id": "py.async.eventloop",
      "sections": [
        {
          "path": "handbook/python-backend/02-async-and-concurrency.md",
          "start_line": 5,
          "end_line": 33,
          "heading": "py.async.eventloop — 协程只有让出控制权，事件循环才能服务其他任务",
          "display_title": "协程只有让出控制权，事件循环才能服务其他任务"
        }
      ],
      "questions": "skills/knowledge-interviewer/references/domains/python-backend/questions.md",
      "sources": "skills/knowledge-interviewer/references/domains/python-backend/sources.md",
      "materials": "materials/python-backend/README.md"
    }
  }
}
```

## python-backend-boundary

- selected_domain: "python-backend"
- selected_point_id: "py.async.execution"
- actions_asked: 1
- state_action: "none; synthetic fixture only; no real .local reads or learning-state writes"
- external_sync: false

### response.txt

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-4-python-boundary/with_skill/run-1/outputs/response.txt`

```text
### 结论
不对：并非所有 Python 构建都启用 GIL，`asyncio.to_thread` 也不自动把纯 Python CPU 计算变成多核并行。

### 机制
| 条件 | 执行边界 |
|---|---|
| 常规启用 GIL 的 CPython | 同一进程的多个线程不能同时执行 Python 字节码；`to_thread` 主要用于卸载阻塞 I/O，不能据此断言纯 Python 计算多核加速。 |
| 释放 GIL 的原生扩展 | 计算可能在线程间多核并行，但这不等于纯 Python 循环也能如此。 |
| CPython 3.13 起的可选 free-threaded 构建 | 不是所有安装的默认模式；运行配置或不兼容扩展可能启用 GIL。实际禁用 GIL 时线程可并行，共享状态仍需同步。 |
| 启用 GIL 时的纯 Python CPU 任务 | 可考虑进程池，代价是序列化、进程通信与额外内存，收益需在目标环境测量；[按目标构建与工作类型选择协程、线程或进程](handbook/python-backend/02-async-and-concurrency.md#L98-L112)。 |

### 验证
假设使用启用 GIL 的 CPython 3.11，要多核并行运行互不共享状态的纯 Python 计算，你会选线程池还是进程池？
```

### execution.json

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-4-python-boundary/with_skill/run-1/outputs/execution.json`

```json
{
  "selected_domain": "python-backend",
  "selected_point_id": "py.async.execution",
  "actions_asked": 1,
  "state_action": "none; synthetic fixture only; no real .local reads or learning-state writes",
  "external_sync": false,
  "public_reads": [
    {"path": "skills/knowledge-interviewer/SKILL.md", "start_line": 1, "end_line": 232, "via": "Read"},
    {"path": "skills/knowledge-interviewer/evals/python-backend/cases.json", "start_line": 9, "end_line": 9, "via": "Grep; selected prompt and fixture only"},
    {"path": "skills/knowledge-interviewer/references/domains/python-backend/map.md", "start_line": 1, "end_line": 117, "via": "Read"},
    {"path": "skills/knowledge-interviewer/references/domains/python-backend/sources.md", "start_line": 1, "end_line": 116, "via": "Read"},
    {"path": "skills/knowledge-interviewer/references/learning-flow.md", "start_line": 1, "end_line": 40, "via": "Read"},
    {"path": "skills/knowledge-interviewer/references/domains/python-backend/questions.md", "start_line": 168, "end_line": 168, "via": "Grep; heading location"},
    {"path": "skills/knowledge-interviewer/scripts/learning_content.py", "start_line": 1, "end_line": 52, "via": "Read"},
    {"path": "skills/knowledge-interviewer/references/domains/python-backend/questions.md", "start_line": 168, "end_line": 185, "via": "Read"},
    {"path": "skills/knowledge-interviewer/references/output-format.md", "start_line": 1, "end_line": 60, "via": "Read"},
    {"path": "catalog.json", "start_line": 1, "end_line": 17, "via": "learning_content.py"},
    {"path": "skills/knowledge-interviewer/references/domains/python-backend/map.md", "start_line": 1, "end_line": 116, "via": "learning_content.py"},
    {"path": "handbook/python-backend/01-python-foundations.md", "start_line": 1, "end_line": 158, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/02-async-and-concurrency.md", "start_line": 1, "end_line": 112, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/03-api-and-lifecycle.md", "start_line": 1, "end_line": 91, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/04-storage-and-retrieval.md", "start_line": 1, "end_line": 122, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/05-jobs-and-distribution.md", "start_line": 1, "end_line": 75, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/06-python-agent.md", "start_line": 1, "end_line": 62, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/07-operations-and-delivery.md", "start_line": 1, "end_line": 60, "via": "learning_content.py; public section scan"},
    {"path": "handbook/python-backend/02-async-and-concurrency.md", "start_line": 98, "end_line": 112, "via": "Read; located teaching section"}
  ]
}
```

## python-backend-privacy

- selected_domain: "python-backend"
- selected_point_id: null
- actions_asked: 0
- state_action: "not_saved_read_only; no_real_profile_read; no_init; no_permission_change; no_path_bypass"
- external_sync: false

### response.txt

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-5-python-privacy/with_skill/run-1/outputs/response.txt`

```text
### 状态
未保存学习进度、错题或会话总结；未向外部同步。

### 记录
| 项目 | 本次讨论小结 |
|---|---|
| 实践证据 | 仅自述复制示例并跑通；未提供执行日志，运行结果未验证。 |
| 掌握证据 | 未回答原理问题；独立解释与延迟迁移未验证，不能据此判 A，也不能判不会。 |
| 记录边界 | 原题未提供；未更新 30 个知识点的成绩，未新增错题或复习日期。 |
| 下一步 | 下次选一个复制过的示例，脱离示例独立解释它的执行过程。 |

### 入口
本轮为只读运行，无实际写入授权，因此没有新记录入口。
```

### execution.json

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-5-python-privacy/with_skill/run-1/outputs/execution.json`

```json
{
  "selected_domain": "python-backend",
  "selected_point_id": null,
  "actions_asked": 0,
  "state_action": "not_saved_read_only; no_real_profile_read; no_init; no_permission_change; no_path_bypass",
  "external_sync": false,
  "public_reads": [
    {
      "path": "skills/knowledge-interviewer/SKILL.md",
      "start_line": 1,
      "end_line": 232
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "start_line": 10,
      "end_line": 10,
      "scope": "Grep -o 仅匹配案例标识 python-backend-privacy"
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "start_line": 7,
      "end_line": 12,
      "scope": "Grep -o 仅提取 prompt 与 fixture 字符串；执行的是第 10 行案例"
    },
    {
      "path": "skills/knowledge-interviewer/references/output-format.md",
      "start_line": 1,
      "end_line": 60
    },
    {
      "path": "skills/knowledge-interviewer/references/sprint-learning.md",
      "start_line": 1,
      "end_line": 60
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/map.md",
      "start_line": 1,
      "end_line": 117
    }
  ]
}
```

## python-backend-skip

- selected_domain: "python-backend"
- selected_point_id: "py.async.eventloop"
- actions_asked: 1
- state_action: "none; honor the requested topic switch without grading the unanswered objects question or changing progress, mistakes, preferences, or review scheduling; no real local state read"
- external_sync: false

### response.txt

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-6-python-skip/with_skill/run-1/outputs/response.txt`

```text
好，对象这点先跳过，暂不判档，进入 Python 事件循环。

假设在 Python 3.11+ 中，同一个事件循环线程正在执行某个协程里的 `time.sleep(2)`，另一个协程已就绪。

这两秒内，另一个协程能否由该事件循环线程继续执行？
```

### execution.json

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-6-python-skip/with_skill/run-1/outputs/execution.json`

```json
{
  "selected_domain": "python-backend",
  "selected_point_id": "py.async.eventloop",
  "actions_asked": 1,
  "state_action": "none; honor the requested topic switch without grading the unanswered objects question or changing progress, mistakes, preferences, or review scheduling; no real local state read",
  "external_sync": false,
  "public_reads": [
    {
      "path": "skills/knowledge-interviewer/SKILL.md",
      "line_ranges": [[1, 232]]
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "line_ranges": [[11, 11]]
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/map.md",
      "line_ranges": [[1, 117]]
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/questions.md",
      "line_ranges": [[123, 138]]
    }
  ]
}
```

## python-backend-format

- selected_domain: "python-backend"
- selected_point_id: "py.agent.tools"
- actions_asked: 1
- state_action: "none_read_only"
- external_sync: false

### response.txt

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-3-python-tool-authorization/with_skill/run-1/outputs/response.txt`

```text
### 结论
不能执行：schema 校验通过只说明参数合规，不代表拥有删除权限。

### 机制
| 环节 | 边界 |
|---|---|
| 检索文档 | 是不可信的数据，不是授权来源；文档里的指令不能扩大权限。 |
| 参数校验 | 检查字段、类型等输入约束，不能替代业务授权。 |
| 执行器 | 服务端检查工具白名单及执行时的身份、对象范围与当前权限；本轮仅允许只读，拒绝调用 `delete_file`。 |
| 写操作审批 | 必须另获显式授权，绑定具体动作、参数、对象版本和有效期，执行时重新检查；见[allowlist、schema 与当前授权缺一不可](handbook/python-backend/06-python-agent.md#L5-L31)。 |

### 验证
假设模型建议调用参数合法的 `send_email`，当前仍只有只读授权：可以执行吗？
```

### execution.json

来源：`skills/knowledge-interviewer-workspace/iteration-1/eval-3-python-tool-authorization/with_skill/run-1/outputs/execution.json`

```json
{
  "selected_domain": "python-backend",
  "selected_point_id": "py.agent.tools",
  "actions_asked": 1,
  "state_action": "none_read_only",
  "external_sync": false,
  "public_reads": [
    {
      "path": "skills/knowledge-interviewer/SKILL.md",
      "start_line": 1,
      "end_line": 232
    },
    {
      "path": "skills/knowledge-interviewer/evals/python-backend/cases.json",
      "start_line": 12,
      "end_line": 12,
      "location_result": "python-backend-format 的 prompt 与 fixture；定位搜索同时返回本文件第 7–11 行的案例字段，未读取 rubric 或其他运行产物。"
    },
    {
      "path": "skills/knowledge-interviewer/scripts/learning_content.py",
      "start_line": 1,
      "end_line": 52,
      "location_result": {
        "domain": "python-backend",
        "point_id": "py.agent.tools",
        "sections": [
          {
            "path": "handbook/python-backend/06-python-agent.md",
            "start_line": 5,
            "end_line": 31,
            "heading": "py.agent.tools — allowlist、schema 与当前授权缺一不可",
            "display_title": "allowlist、schema 与当前授权缺一不可"
          }
        ],
        "questions": "skills/knowledge-interviewer/references/domains/python-backend/questions.md",
        "sources": "skills/knowledge-interviewer/references/domains/python-backend/sources.md",
        "materials": "materials/python-backend/README.md"
      }
    },
    {
      "path": "skills/knowledge-interviewer/references/learning-flow.md",
      "start_line": 1,
      "end_line": 40
    },
    {
      "path": "skills/knowledge-interviewer/references/output-format.md",
      "start_line": 1,
      "end_line": 60
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/map.md",
      "start_line": 1,
      "end_line": 117
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/questions.md",
      "start_line": 401,
      "end_line": 414,
      "location_result": "按 py.agent.tools 标题定位后读取对应题链；标题搜索未读取其他题链正文。"
    },
    {
      "path": "skills/knowledge-interviewer/references/domains/python-backend/sources.md",
      "start_line": 1,
      "end_line": 116
    },
    {
      "path": "handbook/python-backend/06-python-agent.md",
      "start_line": 5,
      "end_line": 31
    }
  ]
}
```
