# 领域包：frontend — 知识图谱

结构层核验：2026-11-09。19 个稳定 ID，覆盖浏览器、JS/TS、React 状态、HTTP/SSE、Agent 审批与工件、安全、性能、无障碍、测试与交付。保留前端方案全部 13 个候选 ID，另补 6 个基础 ID。

阅读正文：[前端卷](../../../../../handbook/frontend/README.md)。题库见 [questions.md](questions.md)，官方证据与变化边界见 [sources.md](sources.md)。阅读图谱见 [knowledge-map.md](../../../../../handbook/frontend/knowledge-map.md)，它只维护依赖说明，不复制本表。

## 基础层 L1

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `fe.web.semantic` | L1 | HTML 语义与事件 | 原生控件提供哪些键盘/焦点契约；target/currentTarget 与嵌套动作 | 点击能用就是按钮；加 role 自动补齐行为 |
| `fe.css.layout` | L1 | CSS 约束与响应式 | 盒模型、级联、Flex/Grid 自动最小尺寸、滚动容器 | width 100% 一定不溢出；hidden 等于修复 |
| `fe.web.rendering` | L1 | 浏览器渲染路径 | JS/样式/布局/绘制成本，读写交错为何可能同步布局 | fetch 快就是界面快；rAF 能消除重计算 |
| `fe.js.value` | L1 | 值、对象身份与拷贝 | 浅拷贝后哪些仍共享；const、原型与自有属性的边界 | spread 深拷贝；const 对象不可变 |
| `fe.js.scope` | L1 | 作用域与闭包 | 捕获绑定、var/let、this 与模块作用域；回调读的是哪份状态 | 回调总拿最新值；闭包总冻结值 |
| `fe.js.async` | L1 | 异步与取消 | 任务/微任务、Promise 组合、超时与底层取消、timer 非准时 | race 超时停止工作；all 拒绝自动取消其余任务 |
| `fe.ts.contract` | L1 | 静态类型与输入边界 | unknown 校验、可辨识联合、穷尽处理与业务语义的边界 | as 能验证 JSON；类型合法即授权合法 |

## 组合层 L2

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `fe.web.lifecycle` | L2 | 资源与异步生命周期 | 所有者、cleanup、scope/revision 复验、abort 的边界 | 防抖或 abort 自动消除过期提交 |
| `fe.state.task` | L2 | 任务与视图状态 | 服务端任务/连接/编辑分离；快照游标；乐观更新按操作回滚 | EOF 就完成；关页面就取消 |
| `fe.render.react` | L2 | 渲染快照与身份 | 累计更新、key、Effect 同步与清理、SSR 首次一致 | 空依赖万能；下标 key 不影响编辑状态 |
| `fe.web.http` | L2 | HTTP 与浏览器权限 | fetch HTTP 错误、CORS/CSRF/凭据、缓存、幂等重试 | no-cors 解跨域；CORS 就是授权；no-cache 不存储 |
| `fe.security.output` | L2 | 不可信输出与执行入口 | 文本/HTML/URL/资源/iframe/message 各自边界；XSS 与注入区分 | 删 script 就安全；CSP 替代清洗 |
| `fe.a11y.status` | L2 | 焦点与状态感知 | 键盘旅程、对话框焦点、分阶段播报、虚拟列表可达性 | 每 token assertive 更及时；扫描通过即无障碍 |

## 系统层 L3

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `fe.stream.recovery` | L3 | 事件流恢复 | UTF-8/帧边界、run/seq、重放去重、缺口、EOF 与快照一致 | read 一次一事件；文本去重；自动重连即 exactly-once |
| `fe.approval.scope` | L3 | 审批作用域 | 动作/对象/参数/版本绑定、过期、服务端一次性消费 | approved=true 授权所有后续动作；防双击等于幂等 |
| `fe.perf.streaming` | L3 | 流式性能 | 合并、增量解析、虚拟列表、背压、滚动锚点、交互指标 | render 少一定快；缓冲无限；只看 tokens/s |
| `fe.quality.delivery` | L3 | 构建与兼容交付 | lock/环境、模块与懒加载、资产缓存、旧客户端、灰度回滚 | 有 lock 万能；旧 chunk 随新版本删除 |
| `fe.eval.journey` | L3 | 用户旅程验证 | 不同层的独立期望、故障注入、确定性恢复与随机模型评测 | 截图等于功能；重试绿就可靠；mock 授权证明服务端 |
| `fe.product.artifact` | L3 | 工件与多模态 | 上传/处理分阶段、引用版本、条件保存、dirty 数据保护、资源回收 | HTTP 200 即可检索；最后响应代表最新内容 |

## 直接依赖

L1 无本领域前置。下表是组题依据；同层仍可存在明确前置，不用难度标签替代依赖。

| ID | 先检查的前置 |
|---|---|
| `fe.web.lifecycle` | `fe.js.scope`、`fe.js.async` |
| `fe.state.task` | `fe.js.value`、`fe.ts.contract` |
| `fe.render.react` | `fe.js.value`、`fe.js.scope`、`fe.web.lifecycle` |
| `fe.web.http` | `fe.js.async`、`fe.ts.contract` |
| `fe.security.output` | `fe.web.semantic`、`fe.ts.contract`、`fe.web.http` |
| `fe.a11y.status` | `fe.web.semantic`、`fe.css.layout`、`fe.state.task` |
| `fe.stream.recovery` | `fe.js.async`、`fe.ts.contract`、`fe.web.http`、`fe.state.task` |
| `fe.approval.scope` | `fe.state.task`、`fe.web.http` |
| `fe.perf.streaming` | `fe.css.layout`、`fe.web.rendering`、`fe.render.react`、`fe.stream.recovery` |
| `fe.quality.delivery` | `fe.web.http`、`fe.ts.contract`、`fe.render.react` |
| `fe.eval.journey` | `fe.stream.recovery`、`fe.approval.scope`、`fe.security.output`、`fe.a11y.status` |
| `fe.product.artifact` | `fe.web.lifecycle`、`fe.state.task`、`fe.web.http`、`fe.security.output` |

## 组题与首次定位

先读 `.local/learning/frontend/progress.md` 与 `mistakes.md`；到期复习优先，其次 D 档基础空缺，再沿依赖引入新点。没有进度行才做首次定位，仓库阅读清单不作为已测状态。

首次定位三题**逐轮**问：① `fe.js.value` 测浅拷贝共享；② `fe.web.lifecycle` 测过期提交；③ `fe.stream.recovery` 测任务游标。第①题未建立值模型就先补基础，不能把三个问题同轮发出。React 指定题先确认用户有 React 经验；无经验先学通用生命周期，不按框架语法扣分。

每次计划 5–10 题但深度优先，围绕同一链：async → lifecycle → state → stream；或 semantic → output → approval。跨 Agent/Go 的内容仅作机制桥梁，领域进度仍分别记，不因会 Agent 就自动给前端 A。

判档按共享 Skill：A 要能解释保证在哪一层、适用条件与代价；B 结论对但缺机制；C 复述术语或命中错误模型；D 不知道或答错。题干先定义 run、seq、revision、EOF 等术语，每轮只要求一个作答动作。
