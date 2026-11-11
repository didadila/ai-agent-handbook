# 前端领域证据索引

> verified_at: 2026-11-09
> 下次例行核验：2026-11-23；涉及当前版本或浏览器支持情况时即时重验。

2026-11-10抽查：TypeScript官方Everyday Types仍明确断言在编译时移除、没有运行时检查；React useEffect文档仍用cleanup中的ignore标记阻止过期响应提交。仅复核这两个切面，不代表全表重新核验。React动态入口此次显示v19.3，示例机制不应被误记为只在某一小版本有效。

只使用标准制定方、语言/框架维护方、浏览器文档、工具官方文档与 OWASP。正文案例、事件字段和状态机是本书原创教学设计，不声称是规范定义或真实事故统计。标准证明标准内容，工具文档证明工具契约；它们不证明本项目已完成浏览器与服务端验收。

## 知识点到证据

| ID | 支持的稳定机制 | 证据 | 不外推的边界 |
|---|---|---|---|
| `fe.web.semantic` | 键盘可访问交互与原生语义 | [F1] | role 不自动实现键盘行为 |
| `fe.css.layout` | 盒模型与自动最小尺寸 | [F2][F3] | 布局片段只针对所述约束，不是任意页面通解 |
| `fe.web.rendering` | 渲染路径与强制同步布局 | [F4][F5] | 不宣称每次读取都触发布局；需性能轨迹确认 |
| `fe.js.value` | 展开是浅复制 | [F6] | 不把 JSON 克隆当任意对象深复制 |
| `fe.js.scope` | 闭包捕获词法环境，模块有作用域 | [F7][F28] | React 快照结合框架文档理解，不说所有闭包冻结值 |
| `fe.js.async` | 执行模型、race结果、协作取消 | [F8][F9][F10] | 服务端取消与回滚属于应用契约 |
| `fe.ts.contract` | 断言无运行时检查，联合收窄 | [F11][F12] | schema不证明对象权限与业务正确性 |
| `fe.web.lifecycle` | cleanup避免过期响应提交 | [F13][F10] | abort只是减少工作，不独立证明无旧回调 |
| `fe.state.task` | UI需显式状态；外部同步有生命周期 | [F14][F13] | 本书任务/连接/编辑三域是工程设计，非React标准状态机 |
| `fe.render.react` | 快照、身份、Effect与hydration | [F13][F14][F15][F16][F34] | 初次挂载额外Effect循环限定开发环境、根部Strict Mode；子树启用边界按官方说明 |
| `fe.web.http` | fetch、CORS、缓存契约 | [F17][F18][F19] | CORS不是服务端对象授权，no-cache不是no-store |
| `fe.stream.recovery` | SSE帧/重连/ID与流读取 | [F20][F21] | run/连续seq/快照是本书应用协议，不是SSE强制字段 |
| `fe.approval.scope` | 服务端执行授权与关键参数绑定 | [F22] | 哈希、按钮或一次确认均不能替代业务授权 |
| `fe.security.output` | 上下文相关XSS防护与sandbox | [F23][F24] | CSP不是唯一防线，沙箱要按origin/出口验证 |
| `fe.product.artifact` | 文件验证、条件更新、资源回收 | [F25][F26][F27] | 上传成功与检索就绪是不同阶段；工件状态由应用定义 |
| `fe.perf.streaming` | 交互延迟与布局成本 | [F29][F5] | 不把文档示例数字或单次跑分作通用门限 |
| `fe.a11y.status` | 状态播报与模态焦点模式 | [F30][F31][F1] | APG是实现模式；自动扫描不证明完整符合性 |
| `fe.quality.delivery` | 锁文件安装与HTTP缓存 | [F32][F19][F28] | lock不固定全部环境；灰度兼容窗口由项目设计 |
| `fe.eval.journey` | 验用户可见行为、隔离与可靠等待 | [F33] | Node实验不证明浏览器、安全后端或性能指标 |

## 官方来源

以下均于 verified_at 打开核验；访问日期不是文章发布时间。

- **[F1]** MDN，[Keyboard accessible](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG/Keyboard)。
- **[F2]** MDN，[The box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)。
- **[F3]** MDN，[min-width](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/min-width)。
- **[F4]** MDN，[Critical rendering path](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Critical_rendering_path)。
- **[F5]** web.dev，[Avoid large layouts and layout thrashing](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing)。
- **[F6]** MDN，[Spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)。
- **[F7]** MDN，[Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)。
- **[F8]** MDN，[JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model)。
- **[F9]** MDN，[Promise.race](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race)。
- **[F10]** MDN，[AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)。
- **[F11]** TypeScript，[Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)。
- **[F12]** TypeScript，[Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)。
- **[F13]** React，[useEffect](https://react.dev/reference/react/useEffect)。
- **[F14]** React，[State as a Snapshot](https://react.dev/learn/state-as-a-snapshot)。
- **[F15]** React，[Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)。
- **[F16]** React，[hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)。
- **[F17]** MDN，[Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)。
- **[F18]** MDN，[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)。
- **[F19]** MDN，[HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)。
- **[F20]** WHATWG HTML，[Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html)。
- **[F21]** MDN，[Using readable streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams)。
- **[F22]** OWASP，[Transaction Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)。
- **[F23]** OWASP，[XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)。
- **[F24]** MDN，[iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)。
- **[F25]** OWASP，[File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)。
- **[F26]** MDN，[If-Match](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Match)。
- **[F27]** MDN，[revokeObjectURL](https://developer.mozilla.org/en-US/docs/Web/API/URL/revokeObjectURL_static)。
- **[F28]** MDN，[JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)。
- **[F29]** web.dev，[Optimize INP](https://web.dev/articles/optimize-inp)。
- **[F30]** W3C WAI，[Understanding status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)。
- **[F31]** W3C WAI，[Modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)。
- **[F32]** npm CLI v11 文档，[npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/)。这是引用版本，不声明它是最新 CLI。
- **[F33]** Playwright，[Best Practices](https://playwright.dev/docs/best-practices)。
- **[F34]** React，[StrictMode](https://react.dev/reference/react/StrictMode)。2026-11-09追加核验，明确开发环境与根部/子树启用区别。

## 易变事实与使用规则

正文不锁定React最新版本、浏览器支持矩阵、包体积数字、INP上线阈值或工具价格。遇到这些问题先打开官方当前文档，注明目标环境、版本与访问日期。候选/实验API不作为稳定知识点的必答项。若支持情况不明，直接把问题改成给定环境下的机制题。

牛客面经仅作场景线索，沿用[Agent 面经映射](../ai-agent/interview-bank.md)中的 partial 标注，不把摘要当完整原题。力扣 [2637](https://leetcode.cn/problems/promise-time-limit/)、[2622](https://leetcode.cn/problems/cache-with-time-limit/)、[2627](https://leetcode.cn/problems/debounce/)为经典局部练习，迁移见[增量工程练习](../../../../../handbook/ai-agent/08-增量工程练习.md)，题目通过不替代工程验收。
