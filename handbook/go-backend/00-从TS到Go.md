# 第 0 章 · 从 TS 到 Go：先换掉六个默认假设

> **30 秒速览**：TS 默认共享，Go 默认拷贝；TS 有 `undefined`，Go 只有零值；TS 的数组是对象，Go 的 slice 是描述符。用 TS 的直觉写 Go，代码能编译，但会在「谁改了谁的数据」「为什么这里 panic」上反复翻车。本章不引入新知识点，只把六个默认假设换掉，作为第 1 章的前置。

## 0.1 赋值是拷贝，不是共享

**结论**：`b := a` 在 Go 里是整块复制。想共享，必须显式用指针、slice、map 或 chan。

**机制**：Go 的变量就是一块内存。struct、array 赋值时按值复制；只有指针、slice、map、chan、func、interface 这几种类型的值本身是「描述符」，复制描述符后仍指向同一份底层数据。

```go
type User struct{ Name string }

a := User{Name: "a"}
b := a            // 复制整个 struct
b.Name = "b"      // a.Name 仍然是 "a"
```

TS 里 `const b = a` 改 `b` 就是改 `a`。Go 里不成立，这是最常见的第一个跟头。

**判据**：**这个函数需不需要改调用方的数据？** 需要，传 `*T`；不需要，传值——传值更安全，改坏了也只影响副本。

## 0.2 零值不是「没有值」

**结论**：Go 的每个类型都有零值，没有 `undefined`。零值能参与运算，所以「没传」和「传了零值」在类型层面分不开。

```go
var n int             // 0
var s string          // ""
var p *User           // nil
var m map[string]int  // nil
var sl []int          // nil
```

`nil` 也不是一个统一的值，而是六种可 nil 类型的零值，行为各不相同：

| 类型 | nil 时能做什么 | nil 时不能做什么 |
|---|---|---|
| `*T` | 比较 `p == nil` | 解引用 `p.Field` → panic |
| `[]T` | `len` / `range` / `append` 都正常 | 索引读写（len 为 0，任何下标都越界） |
| `map[K]V` | 读返回零值、`len`、`range`、`delete` 都正常 | 写入 → panic，必须先 `make` |
| `chan T` | 比较 | 收发永久阻塞，`close` panic |
| `func()` | 比较 | 调用 panic |
| `interface{}` | 与 `nil` 比较 | 调用方法 panic；单值断言 `x.(T)` panic（`v, ok := x.(T)` 返回 `false`，不 panic） |

两个必须当场记住的例子：

```go
var m map[string]int
m["a"] = 1          // panic: assignment to entry in nil map

var s []int
s = append(s, 1)    // 正常，s 变成 [1]
```

区别在于：map 的零值是「一张表都没建」，写入没有桶可写；而 `append` 是函数，发现 cap 不够会自己分配新数组，不依赖原数组存在。

**判据**：**这个变量接下来会被写吗？** 会写，就必须先把它分配出来。Go 不会替你隐式创建 `{}`。

## 0.3 slice 是描述符，不是数组

**结论**：slice 的值是 `{ptr, len, cap}` 三个字段。赋值、传参复制的是这三个字段，底层数组仍共享——但只在 `[0, cap)` 范围内。

```
┌─────┬─────┬─────┐
│ ptr │ len │ cap │   ← 赋值、传参拷贝这三个字段
└──┬──┴─────┴─────┘
   └──→ 底层数组（这块才是共享的）
```

两个动作要分开判断：

| 动作 | 是否影响原切片 |
|---|---|
| `s[i] = x` / `s[i].Field = x` | 会，只要下标在 len 内（改的是底层数组） |
| `append(s, x)` | 看 cap：有余量写进原数组，没余量新分配 |

```go
all := []Item{{1, "a"}, {2, "b"}, {3, "c"}}
part := all[:2]                 // len=2, cap=3
part[0].Name = "changed"        // all[0].Name 也变了
part = append(part, Item{4, "d"}) // cap 够，覆盖 all[2]

clipped := all[:2:2]            // 三索引切片，把 cap 夹成 2
clipped = append(clipped, Item{5, "e"}) // cap 不够，新分配，all 不受影响
```

还有一条：`append` 返回的是**新的切片头**，不赋回去等于没写。

```go
var s []int
append(s, 1)        // 编译不过：append(...) is not used
s = append(s, 1)    // 必须赋回新的切片头
```

**判据**：**这次 append 复用的是谁的容量？** 如果答案不是「只有我自己」，就复制一份，或者用 `items[:n:n]` / `slices.Clip` 把 cap 夹掉。

## 0.4 错误是值，不是异常

**结论**：Go 没有 try/catch，错误是普通返回值，必须显式处理。

```go
u, err := find(1)
if err != nil {
    return fmt.Errorf("find user %d: %w", 1, err)
}
```

- 包装用 `%w`，保留错误链；
- 判断用 `errors.Is`（哨兵错误）或 `errors.As`（错误类型）；
- 多返回值是常态，`(T, error)` 是最常见的签名；
- 不要用字符串比较判断错误类型。

**判据**：**调用方能不能用 `errors.Is/As` 判出这个错误？** 只能靠字符串匹配，说明错误没有设计好。

## 0.5 没有 class：struct + 方法 + 隐式接口

**结论**：数据放 struct，行为挂方法，抽象用 interface；接口是隐式实现，不写 `implements`。

```go
type Store struct{ db *sql.DB }

func (s *Store) Get(id int) (*User, error) { /* ... */ }

type Reader interface {
    Get(id int) (*User, error)
}
```

`*Store` 自动满足 `Reader`，只要方法签名对得上。复用靠嵌入字段（组合），不靠继承。

接收者判据：**这个方法要改字段吗？** 要改、或结构较大，用指针接收者 `*T`；只读的小值可以用 `T`。同一个类型不要混用两种接收者。

## 0.6 并发不是异步

**结论**：goroutine 不是 Promise，没有 `await`。它就是另开一条执行线，什么时候结束要你自己保证。

```go
go func() {
    defer wg.Done()
    // 必须有明确的退出路径：返回、context 取消、channel 关闭
}()
```

先记住一句：**每个 goroutine 都必须有退出条件和数量上限。** 细节在第 2 章。

## 0.7 一张对照表

| TS / JS | Go |
|---|---|
| 对象赋值共享 | 默认拷贝，共享要显式 |
| `undefined` 表示缺失 | 零值 + 指针 / Null 类型 |
| 数组、对象都是引用 | slice / map 是描述符，struct 是值 |
| `try / catch` | `if err != nil` |
| `class` + `implements` | struct + 方法 + 隐式接口 |
| `Promise` / `await` | goroutine + channel + context |
| 假值判断（`if (x)`） | 条件必须是 bool，`if x` 编译不过 |
| 隐式类型转换 | 没有，`int` 与 `int64` 不通用 |

几条编译期就会拦住你的规则：变量或 import 声明了不用会**编译失败**；`:=` 只能在函数内用；首字母大写才是导出。

## 0.8 自测题

不看上面，直接答。答不出来的回对应小节。

1. `part := all[:2]` 之后执行 `part[0].Name = "x"`，`all[0].Name` 是什么？再执行 `part = append(part, item)`，`all` 会怎样？把两个动作分开解释。
2. 改成 `all[:2:2]` 后，上面两个动作的结果分别是什么？
3. `var m map[string]int; m["a"] = 1` 和 `var s []int; s = append(s, 1)`，为什么一个 panic、一个正常？
4. 写 `func Double(nums []int) []int`，返回翻倍后的新切片，要求调用方的 `nums` 一个字节都不能变。说明你的实现为什么不会踩到 cap 的坑。
5. 一个方法只读字段、结构只有两个 int，应该用值接收者还是指针接收者？如果之后要加一个修改字段的方法，怎么办？
