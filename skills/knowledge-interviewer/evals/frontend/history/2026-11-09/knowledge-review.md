# 前端知识结论核验

核验日期：2026-11-09。范围：覆盖19点的24条代表性结论，不等于对每个句子逐字认证。原F1–F33均重新打开，另核验F34 StrictMode。证据编号和URL见[来源索引](../../../../references/domains/frontend/sources.md)。本表只写核验者的概括，不复制大段原文。

“支持”表示所列官方来源直接说明相关机制；“设计审查”表示本书自己的应用协议，检查内部一致性与可执行例子，不声称由React/SSE标准规定；“收窄后支持”保留发现的问题与修订。

| 编号 | 知识点 | 被核验结论 | 证据定位 | 结论与边界 |
|---|---|---|---|---|
| K01 | `fe.web.semantic` | 可点击操作需可聚焦、有交互语义和键盘触发 | F1 Keyboard accessible 的对应小节 | 支持；role不自动提供行为 |
| K02 | `fe.css.layout` | border-box包含padding/border，Flex/Grid自动最小尺寸可能受内容限制 | F2 alternative box model；F3 auto/min-content | 支持；保留scroll container等例外，不说所有auto都等于min-content |
| K03 | `fe.web.rendering` | DOM写后几何读取可能强制布局；rAF不消除计算 | F4渲染路径；F5布局抖动 | 支持；需轨迹判断，不把每次读取都判为强制布局 |
| K04 | `fe.js.value` | 对象展开只复制一层，嵌套对象身份可共享 | F6 Copying and merging objects | 支持；另有可执行例子验证 |
| K05 | `fe.js.scope` | 闭包保留词法环境，共享或逐轮绑定取决于声明 | F7 lexical environment与循环示例 | 支持；var/let结果单独执行验证 |
| K06 | `fe.js.async` | race决定外层结果，不取消其他操作 | F9 Description明确说明losing operations不取消；F10 abort | 支持；用可控deferred验证，不靠timer碰运气 |
| K07 | `fe.ts.contract` | as在编译时移除，不附带运行时验证 | F11 Type Assertions；F12 discriminated unions | 支持；不把联合穷尽检查当未知输入校验 |
| K08 | `fe.web.lifecycle` | cleanup中的ignore/版本检查可拒绝乱序旧响应 | F13 Fetching data with Effects的race conditions说明 | 支持；取消不替代提交前scope检查 |
| K09 | `fe.state.task` | 服务端状态、连接状态、本地取消意图分别表达 | 本书状态表与workbench-core、对应测试 | 设计审查修复：旧表和代码把cancel_requested混进任务status，现独立字段保留权威状态 |
| K10 | `fe.render.react` | 初次Effect额外循环受开发环境和根部StrictMode条件限制 | F34 Note：非根部不额外重跑initial mount；F13 | 收窄后支持；原表只有开发环境边界，现补根部/子树区别 |
| K11 | `fe.render.react` | 状态来自渲染快照，key/位置决定身份，hydration首次内容应一致 | F14、F15、F16 Caveats | 支持；函数式更新不解决跨run污染 |
| K12 | `fe.web.http` | HTTP403/404并不使fetch必然reject | F17检查response状态示例 | 支持；网络与HTTP错误分开处理 |
| K13 | `fe.web.http` | no-cache允许保存但需验证，no-store禁止新存储 | F19 fresh/revalidation/no-store说明 | 支持；no-store不会自动清除早已缓存的响应 |
| K14 | `fe.web.http` | CORS管跨源读取，不替代CSRF和对象授权 | F18 simple requests/form submissions说明 | 支持；不是“所有跨站请求都会被预检拦截” |
| K15 | `fe.stream.recovery` | SSE空行结束帧，支持CR/LF/CRLF，EOF未结束帧不派发 | F20 stream grammar及Parsing an event stream；F21 | 支持；实验严格拒绝坏UTF-8是自身策略，不冒称完整EventSource复刻 |
| K16 | `fe.stream.recovery` | run+连续不可变seq实现去重、缺口和快照恢复 | 本书应用契约与20项协议测试 | 设计审查通过；以事件不可变、连续序号和完整快照为前提，不外推过滤流 |
| K17 | `fe.approval.scope` | 授权与重要参数由服务端绑定和执行，客户端摘要不授予权限 | F22 2.1/2.3及执行控制 | 支持；尚无真实后端，因此不声称服务端授权实现验收通过 |
| K18 | `fe.security.output` | XSS防护按输出上下文处理，CSP是纵深防护 | F23 Output Encoding与Sole Reliance on CSP | 支持；不信模型自述安全 |
| K19 | `fe.security.output` | iframe同源+脚本能力可能削弱sandbox，需按来源限制能力 | F24 sandbox Notes | 支持；没有浏览器逃逸测试，不声称隔离已证明 |
| K20 | `fe.product.artifact` | 上传MIME可伪造；条件保存可用If-Match防旧版本覆盖 | F25 Content-Type Validation；F26条件不匹配返回412；F27资源释放 | 支持；上传与OCR/索引就绪仍是应用自定阶段 |
| K21 | `fe.perf.streaming` | 交互延迟含输入等待、处理与呈现，tokens/s不足以衡量UI | F29 interaction breakdown；F5 | 支持；未运行真实设备性能测量 |
| K22 | `fe.a11y.status` | 状态可无焦点播报；模态关闭通常返回触发控件 | F30 SC4.1.3；F31 keyboard interaction | 支持；触发控件已移除时有合理后续目标例外 |
| K23 | `fe.quality.delivery` | npm ci依赖lock，不匹配时报错；模块有独立作用域 | F32 Description；F28 module scope；F19版本化缓存 | 支持；lock不固定所有外部环境，兼容窗口仍是设计决策 |
| K24 | `fe.eval.journey` | 测用户可见行为，分层证据不能互相冒充 | F33 Testing philosophy；本书验收矩阵 | 支持；Node通过不等于浏览器/读屏/服务端通过 |

结果：21条直接支持，1条收窄后支持，2条应用设计审查通过；没有将设计审查算作规范事实支持率。K09与K10的修订均同步正文，K09另同步示例与测试。另补充原生EventSource的error不暴露HTTP状态、内部Last-Event-ID不等于应用已提交游标，避免调用层从onerror猜测401或丢失未应用数据。

未做的事：未刷新Agent来源索引中全部A2A/OTel/NIST/论文版本；旧领域只做结构、ID与学习状态回归。未将牛客partial摘要升级为完整原文，也未用搜索抓取日期冒称题目发布日期。
