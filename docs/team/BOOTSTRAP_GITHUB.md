# GitHub 初始化与三人协作指南

**仓库目标地址（创建后）：** `https://github.com/zhang-haichao/RecForgetBench`

目前这份模板是**本地文件，不代表已经创建了远程 GitHub 仓库**。

## 1. 项目负责人创建一个空的私有仓库

1. 打开 <https://github.com/new>，仓库名称填 `RecForgetBench`。
2. `Visibility` 选择 **Private**。
3. **不要勾选**初始化 README、.gitignore 或 License（模板已经包含）。
4. 创建后，按下一节一次性推送完整模板。
5. 在 Settings → Collaborators 邀请三名本科生，授予必要的 Write 权限。

项目负责人不需要成为每次 PR 的必需代码审查人。

## 2. 把下载的代码包推送到 GitHub

解压 `RecForgetBench-starter.zip`，在 `RecForgetBench` 目录打开终端，执行：

```bash
git init -b main
git add .
git commit -m "chore: initialize RecForgetBench research platform"
git remote add origin https://github.com/zhang-haichao/RecForgetBench.git
git push -u origin main
```

首次提交后检查 `.gitignore`，保证没有本地 `.env`、原始数据、Checkpoint
等被错误提交。没有配置 Git 姓名/邮箱时先运行 `git config --global user.name`
和 `git config --global user.email`。

## 3. GitHub 仓库设置

- Settings → Branches / Rulesets：针对 `main` 要求 PR、禁止 force push。
- 首次 CI 跑通后，启用必需状态检查 `Python tests and contracts` 与
  `Offline prototype syntax`（显示名称以 GitHub 实际列出的 check 为准）。
- 若当前私有仓库计划允许，要求至少 **1 名同学**审批 PR。
- 在三名学生的 GitHub 用户名确定后，将
  `docs/team/CODEOWNERS.example` 修改为 `.github/CODEOWNERS`。
- 不应强制每次修改都通知项目负责人进行代码审查。
- Settings → General：默认分支为 `main`。

> GitHub 分支保护和 Code Owners 的具体权限与所用套餐有关；如果某项
> 规则不可用，先使用 PR 审核惯例和 CI，后续再完善保护策略。

## 4. 每名学生的开发流程

```bash
git clone https://github.com/zhang-haichao/RecForgetBench.git
cd RecForgetBench
git switch -c feat/12-recmodel-adapter
# 使用 Claude Code 或 Codex，先阅读 AGENTS.md、模块 AGENTS.md 和该 Issue。
# 编码并运行测试后：
git add .
git commit -m "feat(recsys): add verified recommendation adapter"
git push -u origin feat/12-recmodel-adapter
```

然后在 GitHub 网页创建 Pull Request。请替换示例分支编号与提交信息。

**禁止三个人共用同一个本地目录或把所有改动直接推到 main。**

## 5. 第一周的落地方式

- 三名学生先阅读 README、架构、接口和模块所有权文档。
- 使用 `docs/team/FIRST_ISSUES.md` 创建第一批 Issues，并明确负责人。
- 学生 A 提供真实 RecBole 模型训练与推荐接口。
- 学生 B 开发真实 Forget/Retain 划分与 fresh Retrain 对照。
- 学生 C 搭建实际 Web 应用并在跨模块接口准备好后集成。
- 每周演示可运行版本。现有静态 HTML 原型只作为 UI 参考。

## 6. 项目负责人的验收内容

只看阶段性可验证结果：真实运行演示、测试报告、复现步骤、
科学指标的定义与交叉核对结果，不要求阅读每一行代码。
