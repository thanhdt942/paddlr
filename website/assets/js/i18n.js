/*
 * Paddlr landing page i18n dictionary and agent install data.
 * Exposes window.PADDLR_I18N = { SUPPORTED_LOCALES, STRINGS, AGENTS }.
 */

(function () {
  const REPO = "https://github.com/thanhdt942/paddlr";

  const SUPPORTED_LOCALES = ["en", "vi"];

  const STRINGS = {
    en: {
      "meta.title": "Paddlr - Engineering discipline for AI coding agents",
      "meta.description":
        "Paddlr is an open-source set of 57 Agent Skills bringing spec-driven design, persistent project memory, test-driven development, scientific debugging, and code review to Claude Code, Codex, OpenCode, Google Antigravity, and Cursor.",
      "meta.ogTitle": "Paddlr - Simple on the Surface. Sophisticated Underneath.",
      "meta.ogDescription":
        "Open-source set of 57 Agent Skills bringing spec-driven design, persistent project memory, TDD, debugging, and code review to the coding agent you already use.",

      "a11y.skip": "Skip to content",
      "a11y.navPrimary": "Primary",
      "a11y.home": "Paddlr home",
      "a11y.langGroup": "Language",
      "a11y.codingAgent": "Coding agent",

      "nav.paddlrMode": "Paddlr Mode",
      "nav.install": "Install",
      "nav.docs": "Docs",
      "nav.github": "GitHub",

      "hero.tagline": "Simple on the Surface. Sophisticated Underneath.",
      "hero.lead":
        "Open-source set of 57 Agent Skills bringing spec-driven design, persistent project memory, test-driven development, scientific debugging, and code review to Claude Code, Codex, OpenCode, Google Antigravity, and Cursor.",
      "hero.ctaStart": "Get started",
      "hero.ctaMode": "Paddlr Mode",
      "hero.ctaGithub": "View on GitHub",

      "about.title": "What is Paddlr?",
      "about.p1":
        "Paddlr is not a coding agent. It is an open-source plugin of 57 Agent Skills for Claude Code, Codex, OpenCode, Google Antigravity, and Cursor. It keeps your agent reading the codebase first, planning by risk, saving context in <code>docs/paddlr/</code>, and verifying with real command output.",

      "about.pillar1Title": "Persistent project memory",
      "about.pillar1Body":
        "Stores specs, plans, and ADRs in <code>docs/paddlr/</code> so context survives across sessions.",
      "about.pillar2Title": "Reversibility-first autonomy",
      "about.pillar2Body":
        "Small fixes and branch work run directly. High-risk changes always pause for approval.",
      "about.pillar3Title": "Evidence-based verification",
      "about.pillar3Body":
        "Runs real tests, lint, or runtime checks before reporting done.",

      "about.skillsTitle": "Core skills",
      "about.skill.paddlrMode":
        "Single entry point with 22 playbooks and 26 engineering principles loaded on demand.",
      "about.skill.setupHelp":
        "Initialize <code>docs/paddlr/</code> or <code>.paddlr.json</code>, and route questions read-only without running tasks.",
      "about.skill.featureDev":
        "Runs a 5-phase spec-driven feature lifecycle from intake to verified completion.",
      "about.skill.specsPlans":
        "Turns ideas into reviewable specs in <code>docs/paddlr/specs/</code> and contract-first plans in <code>docs/paddlr/plans/</code>.",
      "about.skill.decisionsSync":
        "Writes immutable ADRs in <code>decisions/</code> indexed in <code>DECISIONS.md</code>, and checks docs for drift before a PR.",
      "about.skill.tdd":
        "Enforces strict RED, GREEN, REFACTOR execution with no production code before a failing test.",
      "about.skill.sreDebugging":
        "Reproduces failures, gathers evidence, and tests hypotheses before proposing a fix.",
      "about.skill.reviewInterrogate":
        "Runs independent read-only spec alignment review and adversarial red-teaming.",
      "about.skill.hygiene":
        "Audits stale comments and workarounds, cuts AI prose filler, and turns repeated mistakes into structural checks.",
      "about.skill.releaseCreator":
        "Records release rules in <code>RELEASE.md</code> and authors new validated Agent Skills.",
      "about.footnote":
        "Ships with shared operating rules in <code>AGENTS.md</code> and a session-start hook that loads them automatically.",

      "mode.title": "Paddlr mode",
      "mode.intro":
        "Invoke <code>/paddlr-mode</code> as a single entry point for disciplined sessions. The skill stays lazy-loaded via <code>disable-model-invocation: true</code>, so it adds zero context overhead until you call it.",
      "mode.bundle":
        "<code>paddlr-mode</code> bundles 22 playbooks (feature, bug fix, refactoring, investigation, opening a PR, and more) alongside 26 engineering principles loaded on demand when a trigger matches.",
      "mode.flowTitle": "How a session runs",
      "mode.step1Title": "Restate the goal",
      "mode.step1Body":
        "The agent restates your goal and the smallest change that meets it before touching code.",
      "mode.step2Title": "Classify risk and pick a playbook",
      "mode.step2Body":
        "Assigns Level 1, 2, or 3 based on reversibility and opens the matching playbook.",
      "mode.step3Title": "Track state in plan and native checklist",
      "mode.step3Body":
        "Mirrors active steps from <code>docs/paddlr/plans/</code> into your host's native checklist via <code>ui.todo</code> (<code>TodoWrite</code>, <code>update_steps</code>, <code>update_plan</code>, <code>todowrite</code>, or chat fallback).",
      "mode.step4Title": "Build, verify, and open a PR",
      "mode.step4Body":
        "Implements in verifiable slices, checks the real artifact, runs <code>sync-docs</code> and <code>code-review</code>, and opens a ready-for-review PR.",
      "mode.baseline":
        "Paddlr runs in a single thread using only 5 basic tools (read, write, patch, shell, search). When your host supports subagents, Paddlr can delegate isolated slices while the main agent keeps canonical plan ownership.",

      "install.title": "Install Paddlr",
      "install.intro": "Choose your coding agent, then run each command in order.",
      "install.postNote":
        "After installing, run <code>/setup-paddlr</code> to initialize <code>docs/paddlr/</code> or create a <code>.paddlr.json</code> override. Run <code>/paddlr-help</code> for read-only routing without executing tasks.",
      "install.noscript":
        'The agent selector needs JavaScript. See the <a href="https://github.com/thanhdt942/paddlr#quick-start--installation">installation guide on GitHub</a>.',
      "install.prerequisites": "Prerequisites",
      "install.install": "Install",
      "install.option": "Option",
      "install.step": "Step",
      "install.verify": "Verify",
      "install.planned": "support is planned and not installable yet.",

      "status.supported": "Supported",
      "status.experimental": "Experimental",
      "status.planned": "Planned",

      "usage.title": "Usage",
      "usage.intro":
        "Once installed, describe the task or invoke a slash command. Your agent selects the matching skill and leaves reviewable artifacts in your repository.",
      "usage.promptLabel": "Prompt",
      "usage.ex1Title": "Start a disciplined session with /paddlr-mode",
      "usage.ex1Prompt": "/paddlr-mode Add CSV export to the reports page",
      "usage.ex1Desc":
        "<code>/paddlr-mode</code> restates the goal, classifies risk, writes a spec and plan to <code>docs/paddlr/plans/</code>, verifies on the real artifact, and prepares a clean PR.",
      "usage.ex2Title": "Plan a feature before writing code",
      "usage.ex2Prompt":
        "Draft feature specifications and implementation plan with Paddlr: add CSV export to the reports page",
      "usage.ex2Desc":
        "The agent inspects the repository, asks about real ambiguities, then writes a spec to <code>docs/paddlr/specs/</code> and a step-by-step plan to <code>docs/paddlr/plans/</code>.",
      "usage.ex3Title": "Implement test-first",
      "usage.ex3Prompt":
        "Run TDD to implement the CSV export (RED -> GREEN -> REFACTOR)",
      "usage.ex3Desc":
        "The agent writes a failing test, watches it fail, adds the minimal code to make it pass, and shows real test output at each step.",
      "usage.ex4Title": "Debug with evidence",
      "usage.ex4Prompt":
        "Systematically investigate and debug a failure with sre-debugging: the export job times out",
      "usage.ex4Desc":
        "The agent reproduces the failure, gathers evidence, and tests hypotheses before proposing a fix.",
      "usage.footnote":
        'In Claude Code, skills are also available as slash commands such as <code>/paddlr:writing-specs</code> and <code>/paddlr:paddlr-mode</code>. Read the full <a href="https://github.com/thanhdt942/paddlr/blob/HEAD/docs/guide/README.md">User Guide</a>.',

      "ack.title": "Acknowledgements",
      "ack.body":
        'Paddlr is inspired by and adapts workflows, playbooks, and engineering principles originating from <a href="https://github.com/poteto">Lauren Tan (@poteto)</a> and <a href="https://github.com/cursor/plugins">pstack</a>. Thank you for sharing those ideas openly and shaping how Paddlr brings them to an agent-agnostic, multi-platform setup.',

      "footer.github": "GitHub",
      "footer.guide": "User Guide",
      "footer.license": "License",
      "footer.contributing": "Contributing",
      "footer.notice": "Paddlr is open source under the Apache-2.0 License.",

      "copy.idle": "Copy",
      "copy.done": "Copied",
      "copy.fallback": "Press Ctrl+C",
      "copy.liveDone": "Copied to clipboard",
      "copy.liveFail": "Copy failed. Text selected, press Ctrl+C.",

      "theme.toDark": "Switch to dark mode",
      "theme.toLight": "Switch to light mode",
      "theme.liveDark": "Dark mode enabled",
      "theme.liveLight": "Light mode enabled",

      "lang.liveEn": "Language switched to English",
      "lang.liveVi": "Đã chuyển sang tiếng Việt",
    },

    vi: {
      "meta.title": "Paddlr - Quy trình kỹ thuật chuẩn cho AI coding agent",
      "meta.description":
        "Paddlr là bộ 57 Agent Skills mã nguồn mở giúp AI coding agent viết spec, lập plan, code theo TDD, debug có căn cứ và review kỹ trên Claude Code, Codex, OpenCode, Google Antigravity và Cursor.",
      "meta.ogTitle": "Paddlr - Bên ngoài chill thế, bên trong tinh tế.",
      "meta.ogDescription":
        "Bộ 57 Agent Skills mã nguồn mở giúp coding agent bạn đang dùng làm việc có quy trình, lưu ngữ cảnh lâu dài và luôn kiểm tra thực tế.",

      "a11y.skip": "Chuyển đến nội dung chính",
      "a11y.navPrimary": "Điều hướng chính",
      "a11y.home": "Trang chủ Paddlr",
      "a11y.langGroup": "Ngôn ngữ",
      "a11y.codingAgent": "Coding agent",

      "nav.paddlrMode": "Paddlr Mode",
      "nav.install": "Cài đặt",
      "nav.docs": "Tài liệu",
      "nav.github": "GitHub",

      "hero.tagline": "Bên ngoài chill thế, bên trong tinh tế.",
      "hero.lead":
        "Bộ 57 Agent Skills mã nguồn mở giúp AI coding agent làm việc có quy trình: viết spec, lập plan, code theo TDD, debug có căn cứ và review kỹ trên Claude Code, Codex, OpenCode, Google Antigravity và Cursor.",
      "hero.ctaStart": "Bắt đầu cài đặt",
      "hero.ctaMode": "Paddlr Mode",
      "hero.ctaGithub": "Xem trên GitHub",

      "about.title": "Paddlr là gì?",
      "about.p1":
        "Paddlr không phải là một coding agent mới. Đây là plugin mã nguồn mở gồm 57 Agent Skills gắn thêm vào Claude Code, Codex, OpenCode, Google Antigravity hoặc Cursor, giúp agent đọc kỹ codebase trước khi sửa, lên kế hoạch vừa tầm với độ rủi ro, lưu lại toàn bộ quyết định trong <code>docs/paddlr/</code> và chỉ báo xong khi đã chạy kiểm tra thực tế.",

      "about.pillar1Title": "Lưu ngữ cảnh lâu dài",
      "about.pillar1Body":
        "Lưu spec, plan và ADR trong <code>docs/paddlr/</code> để sang phiên mới không mất ngữ cảnh.",
      "about.pillar2Title": "Tự chủ theo độ rủi ro",
      "about.pillar2Body":
        "Việc nhỏ và tính năng trên branch chạy thẳng. Thay đổi lớn hoặc nguy hiểm luôn chờ bạn duyệt.",
      "about.pillar3Title": "Báo xong có bằng chứng",
      "about.pillar3Body":
        "Luôn chạy test, lint hoặc kiểm tra thực tế và đưa ra kết quả trước khi báo xong.",

      "about.skillsTitle": "Các skill chính",
      "about.skill.paddlrMode":
        "Cổng vào duy nhất gồm 22 playbook và 26 nguyên tắc kỹ thuật, chỉ nạp khi cần.",
      "about.skill.setupHelp":
        "Khởi tạo <code>docs/paddlr/</code> hoặc <code>.paddlr.json</code>, và hỏi đáp định hướng (chỉ đọc, không sửa code).",
      "about.skill.featureDev":
        "Chạy quy trình làm tính năng 5 bước từ lúc chốt yêu cầu đến khi kiểm tra xong.",
      "about.skill.specsPlans":
        "Biến ý tưởng thành spec trong <code>docs/paddlr/specs/</code> và plan từng bước trong <code>docs/paddlr/plans/</code>.",
      "about.skill.decisionsSync":
        "Ghi lại các quyết định kiến trúc (ADR) trong <code>decisions/</code>, tổng hợp ở <code>DECISIONS.md</code> và kiểm tra docs bị lệch trước khi mở PR.",
      "about.skill.tdd":
        "Làm đúng quy trình TDD (RED, GREEN, REFACTOR), luôn viết test fail trước khi viết code chính.",
      "about.skill.sreDebugging":
        "Tái hiện lỗi, thu thập bằng chứng và kiểm tra giả thuyết trước khi sửa.",
      "about.skill.reviewInterrogate":
        "Review code độc lập đối chiếu với spec, và phản biện kỹ các thiết kế có rủi ro cao.",
      "about.skill.hygiene":
        "Dọn comment thừa và code vá tạm, bỏ văn phong máy móc của AI, và biến lỗi lặp lại thành quy tắc kiểm tra tự động.",
      "about.skill.releaseCreator":
        "Ghi lại quy trình release trong <code>RELEASE.md</code> và hỗ trợ tạo Agent Skill mới đúng chuẩn.",
      "about.footnote":
        "Đi kèm sẵn bộ quy tắc làm việc trong <code>AGENTS.md</code> và hook tự động nạp mỗi khi mở phiên mới.",

      "mode.title": "Paddlr mode",
      "mode.intro":
        "Gọi <code>/paddlr-mode</code> khi bạn muốn mở một phiên làm việc bài bản. Skill này chỉ nạp khi bạn gọi (<code>disable-model-invocation: true</code>), nên không tốn context ở các cuộc trò chuyện bình thường.",
      "mode.bundle":
        "<code>paddlr-mode</code> gom sẵn 22 playbook (làm tính năng mới, fix bug, refactor, điều tra lỗi, mở PR...) và 26 nguyên tắc kỹ thuật, chỉ tự nạp khi đúng tình huống.",
      "mode.flowTitle": "Cách một phiên làm việc diễn ra",
      "mode.step1Title": "Chốt lại mục tiêu",
      "mode.step1Body":
        "Agent tóm tắt lại điều bạn cần và cách sửa gọn nhất trước khi đụng vào code.",
      "mode.step2Title": "Đánh giá rủi ro và chọn playbook",
      "mode.step2Body":
        "Phân loại Level 1, 2 hay 3 tùy mức độ ảnh hưởng, rồi mở đúng playbook tương ứng.",
      "mode.step3Title": "Đồng bộ plan với checklist của công cụ",
      "mode.step3Body":
        "Cập nhật tiến độ từ <code>docs/paddlr/plans/</code> sang checklist có sẵn của agent qua <code>ui.todo</code> (<code>TodoWrite</code>, <code>update_steps</code>, <code>update_plan</code>, <code>todowrite</code>, hoặc in ngay trong chat).",
      "mode.step4Title": "Code từng bước, kiểm tra thật và mở PR",
      "mode.step4Body":
        "Chia nhỏ việc để dễ kiểm chứng, chạy test trên sản phẩm thật, rà lại tài liệu bằng <code>sync-docs</code> và <code>code-review</code> rồi mở PR sẵn sàng merge.",
      "mode.baseline":
        "Paddlr chạy trọn vẹn trong một luồng duy nhất chỉ với 5 công cụ cơ bản (đọc, ghi, sửa file, chạy lệnh shell, tìm kiếm). Nếu nền tảng hỗ trợ subagent, Paddlr có thể tách việc ra chạy song song trong khi agent chính vẫn quản lý file plan gốc.",

      "install.title": "Cài đặt Paddlr",
      "install.intro": "Chọn coding agent bạn đang dùng, rồi chạy lần lượt các lệnh bên dưới.",
      "install.postNote":
        "Cài xong, chạy <code>/setup-paddlr</code> để tạo thư mục <code>docs/paddlr/</code> hoặc file cấu hình <code>.paddlr.json</code>. Cần hỏi đường đi nước bước mà không muốn agent sửa code, cứ gõ <code>/paddlr-help</code>.",
      "install.noscript":
        'Trình chọn agent cần JavaScript. Xem <a href="https://github.com/thanhdt942/paddlr#quick-start--installation">hướng dẫn cài đặt trên GitHub</a>.',
      "install.prerequisites": "Yêu cầu trước khi cài",
      "install.install": "Cài đặt",
      "install.option": "Cách",
      "install.step": "Bước",
      "install.verify": "Kiểm tra lại",
      "install.planned": "đang được lên kế hoạch và chưa hỗ trợ cài đặt.",

      "status.supported": "Đã hỗ trợ",
      "status.experimental": "Thử nghiệm",
      "status.planned": "Dự kiến",

      "usage.title": "Cách sử dụng",
      "usage.intro":
        "Cài xong là dùng được ngay. Bạn chỉ cần mô tả việc cần làm hoặc gõ slash command, agent sẽ tự chọn đúng skill và lưu lại spec, plan ngay trong repo.",
      "usage.promptLabel": "Prompt",
      "usage.ex1Title": "Bắt đầu phiên làm việc bài bản với /paddlr-mode",
      "usage.ex1Prompt": "/paddlr-mode Thêm tính năng xuất CSV cho trang báo cáo",
      "usage.ex1Desc":
        "<code>/paddlr-mode</code> chốt lại mục tiêu, đánh giá rủi ro, viết spec và plan vào <code>docs/paddlr/plans/</code>, chạy kiểm tra thực tế rồi chuẩn bị PR gọn gàng.",
      "usage.ex2Title": "Lập spec và plan trước khi viết code",
      "usage.ex2Prompt":
        "Viết spec và plan với Paddlr: thêm tính năng xuất CSV cho trang báo cáo",
      "usage.ex2Desc":
        "Agent đọc codebase, hỏi lại những chỗ còn chưa rõ rồi lưu spec vào <code>docs/paddlr/specs/</code> và plan từng bước vào <code>docs/paddlr/plans/</code>.",
      "usage.ex3Title": "Code theo TDD (viết test trước)",
      "usage.ex3Prompt":
        "Chạy TDD để làm tính năng xuất CSV (RED -> GREEN -> REFACTOR)",
      "usage.ex3Desc":
        "Agent viết test fail trước, chạy xác nhận lỗi, rồi viết đoạn code tối thiểu để pass và in kết quả test ở từng bước.",
      "usage.ex4Title": "Debug có căn cứ",
      "usage.ex4Prompt":
        "Điều tra và fix lỗi bằng sre-debugging: job xuất CSV bị timeout",
      "usage.ex4Desc":
        "Agent tái hiện lại lỗi, thu thập bằng chứng và kiểm tra từng giả thuyết trước khi đề xuất cách sửa.",
      "usage.footnote":
        'Trên Claude Code, bạn có thể gọi trực tiếp bằng slash command như <code>/paddlr:writing-specs</code> hoặc <code>/paddlr:paddlr-mode</code>. Xem thêm trong <a href="https://github.com/thanhdt942/paddlr/blob/HEAD/docs/guide/README.md">Hướng dẫn sử dụng</a>.',

      "ack.title": "Lời cảm ơn",
      "ack.body":
        'Paddlr được truyền cảm hứng và học hỏi rất nhiều từ các quy trình, playbook và nguyên tắc kỹ thuật của chị <a href="https://github.com/poteto">Lauren Tan (@poteto)</a> và dự án <a href="https://github.com/cursor/plugins">pstack</a>. Cảm ơn chị đã chia sẻ rộng rãi những kinh nghiệm quý giá này để Paddlr có thể đưa chúng lên nhiều nền tảng agent khác nhau.',

      "footer.github": "GitHub",
      "footer.guide": "Hướng dẫn sử dụng",
      "footer.license": "Giấy phép",
      "footer.contributing": "Đóng góp",
      "footer.notice": "Paddlr là mã nguồn mở theo giấy phép Apache-2.0.",

      "copy.idle": "Sao chép",
      "copy.done": "Đã chép",
      "copy.fallback": "Nhấn Ctrl+C",
      "copy.liveDone": "Đã sao chép vào bộ nhớ tạm",
      "copy.liveFail": "Không sao chép được. Văn bản đã được bôi đen, hãy nhấn Ctrl+C.",

      "theme.toDark": "Chuyển sang giao diện tối",
      "theme.toLight": "Chuyển sang giao diện sáng",
      "theme.liveDark": "Đã bật giao diện tối",
      "theme.liveLight": "Đã bật giao diện sáng",

      "lang.liveEn": "Language switched to English",
      "lang.liveVi": "Đã chuyển sang tiếng Việt",
    },
  };

  /**
   * status: "supported" | "experimental" | "planned"
   * Shared invariant fields are defined once; localized strings use { en, vi }.
   */
  const AGENTS = [
    {
      id: "claude-code",
      name: "Claude Code",
      status: "supported",
      prerequisites: {
        en: ["Claude Code with plugin support (the /plugin command)."],
        vi: ["Claude Code có hỗ trợ plugin (lệnh /plugin)."],
      },
      methods: [
        {
          label: { en: "One step", vi: "Một bước" },
          note: {
            en: "Run inside a Claude Code session. Adds the Paddlr marketplace and installs the plugin.",
            vi: "Chạy ngay trong phiên Claude Code. Lệnh này thêm marketplace Paddlr và cài đặt plugin.",
          },
          steps: [
            {
              where: "Claude Code",
              cmd: "/plugin install paddlr --marketplace thanhdt942/paddlr",
            },
          ],
        },
        {
          label: { en: "Two steps", vi: "Hai bước" },
          note: {
            en: "For Claude Code versions without the --marketplace flag.",
            vi: "Dành cho các phiên bản Claude Code chưa có cờ --marketplace.",
          },
          steps: [
            { where: "Claude Code", cmd: "/plugin marketplace add thanhdt942/paddlr" },
            { where: "Claude Code", cmd: "/plugin install paddlr@paddlr" },
          ],
        },
      ],
      verify: {
        text: {
          en: "paddlr@paddlr should show as enabled.",
          vi: "paddlr@paddlr sẽ hiển thị ở trạng thái enabled.",
        },
        where: "Terminal",
        cmd: "claude plugin list",
      },
      docs: {
        label: { en: "Installation guide", vi: "Hướng dẫn cài đặt" },
        href: `${REPO}#claude-code`,
      },
    },
    {
      id: "codex",
      name: "Codex",
      status: "supported",
      prerequisites: {
        en: ["OpenAI Codex CLI with plugin support (codex plugin)."],
        vi: ["OpenAI Codex CLI có hỗ trợ plugin (codex plugin)."],
      },
      methods: [
        {
          label: { en: "Codex CLI", vi: "Codex CLI" },
          note: {
            en: "Add the Paddlr marketplace, then install the plugin from it.",
            vi: "Thêm marketplace Paddlr, sau đó cài đặt plugin từ nguồn đó.",
          },
          steps: [
            { where: "Terminal", cmd: "codex plugin marketplace add thanhdt942/paddlr" },
            { where: "Terminal", cmd: "codex plugin add paddlr@paddlr" },
          ],
        },
      ],
      verify: {
        text: {
          en: "paddlr@paddlr should show as installed, enabled.",
          vi: "paddlr@paddlr sẽ hiển thị trạng thái installed, enabled.",
        },
        where: "Terminal",
        cmd: "codex plugin list",
      },
      docs: {
        label: { en: "Installation guide", vi: "Hướng dẫn cài đặt" },
        href: `${REPO}#openai-codex-codex`,
      },
    },
    {
      id: "opencode",
      name: "OpenCode",
      status: "supported",
      prerequisites: {
        en: ["OpenCode CLI.", "Git, to fetch the plugin from GitHub."],
        vi: ["OpenCode CLI.", "Git để tải plugin từ GitHub."],
      },
      methods: [
        {
          label: { en: "OpenCode CLI", vi: "OpenCode CLI" },
          note: {
            en: "Run in your project. Adds Paddlr to .opencode/opencode.json. Add -g to install globally.",
            vi: "Chạy trong thư mục dự án để thêm Paddlr vào .opencode/opencode.json. Thêm cờ -g nếu muốn cài global.",
          },
          steps: [
            {
              where: "Terminal",
              cmd: "opencode plugin paddlr@git+https://github.com/thanhdt942/paddlr.git",
            },
          ],
        },
        {
          label: { en: "Config file", vi: "File cấu hình" },
          note: {
            en: "Or add Paddlr to the plugin list in your opencode.json.",
            vi: "Hoặc thêm trực tiếp Paddlr vào danh sách plugin trong file opencode.json.",
          },
          steps: [
            {
              where: "opencode.json",
              cmd: '{\n  "$schema": "https://opencode.ai/config.json",\n  "plugin": ["paddlr@git+https://github.com/thanhdt942/paddlr.git"]\n}',
            },
          ],
        },
      ],
      verify: {
        text: {
          en: "The agent should call the pdl_bootstrap tool and print Paddlr's operating principles.",
          vi: "Agent sẽ gọi công cụ pdl_bootstrap và in ra các nguyên tắc vận hành của Paddlr.",
        },
        where: "Terminal",
        cmd: 'opencode run "Show me the Paddlr engineering discipline bootstrap context"',
      },
      docs: {
        label: {
          en: "OpenCode details and exposed tools",
          vi: "Chi tiết OpenCode và danh sách công cụ",
        },
        href: `${REPO}/blob/HEAD/.opencode/INSTALL.md`,
      },
    },
    {
      id: "antigravity",
      name: "Antigravity",
      fullName: "Google Antigravity",
      status: "supported",
      prerequisites: {
        en: ["Google Antigravity CLI (agy)."],
        vi: ["Google Antigravity CLI (agy)."],
      },
      methods: [
        {
          label: { en: "agy CLI", vi: "agy CLI" },
          note: {
            en: "Installs the skills, rules, and session-start hook.",
            vi: "Cài đặt bộ skills, rules và hook khởi động phiên.",
          },
          steps: [
            { where: "Terminal", cmd: "agy plugin install https://github.com/thanhdt942/paddlr" },
          ],
        },
      ],
      verify: {
        text: {
          en: "paddlr should be listed as enabled.",
          vi: "paddlr sẽ xuất hiện trong danh sách ở trạng thái enabled.",
        },
        where: "Terminal",
        cmd: "agy plugin list",
      },
      docs: {
        label: { en: "Installation guide", vi: "Hướng dẫn cài đặt" },
        href: `${REPO}#google-antigravity-agy`,
      },
    },
    {
      id: "cursor",
      name: "Cursor",
      status: "supported",
      prerequisites: {
        en: ["Cursor IDE."],
        vi: ["Cursor IDE."],
      },
      methods: [
        {
          label: { en: "Cursor plugin or rules/skills", vi: "Plugin hoặc rules/skills trong Cursor" },
          note: {
            en: "Add Paddlr as a plugin or rules and skills source in Cursor, then load rules/AGENTS.md together with the skills/ directory.",
            vi: "Thêm Paddlr làm plugin hoặc nguồn rules và skills trong Cursor, sau đó nạp rules/AGENTS.md cùng thư mục skills/.",
          },
          steps: [],
        },
      ],
      verify: null,
      docs: {
        label: { en: "Installation guide", vi: "Hướng dẫn cài đặt" },
        href: `${REPO}#cursor`,
      },
    },
  ];

  window.PADDLR_I18N = {
    SUPPORTED_LOCALES,
    STRINGS,
    AGENTS,
  };
})();
