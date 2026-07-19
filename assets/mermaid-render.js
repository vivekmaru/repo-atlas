(function () {
  const startsLikeMermaid = /^(%%\{[\s\S]*?\}%%\s*)?(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|stateDiagram-v2|erDiagram|gantt|journey|pie|gitGraph|mindmap|timeline|quadrantChart|requirementDiagram|packet|sankey-beta|architecture-beta)\b/;

  function collectMermaidBlocks() {
    const blocks = [];

    document.querySelectorAll(".markdown-body pre.mermaid").forEach((block) => {
      blocks.push(block);
    });

    document.querySelectorAll(".markdown-body pre > code").forEach((code) => {
      const source = code.textContent.trim();
      if (!startsLikeMermaid.test(source)) return;

      const pre = code.parentElement;
      const diagram = document.createElement("pre");
      diagram.className = "mermaid";
      diagram.textContent = source;
      diagram.setAttribute("aria-label", "Rendered Mermaid diagram");
      pre.replaceWith(diagram);
      blocks.push(diagram);
    });

    return Array.from(new Set(blocks));
  }

  async function renderMermaid() {
    const blocks = collectMermaidBlocks();
    if (!blocks.length) return;

    if (!window.mermaid) {
      blocks.forEach((block) => {
        const fallback = document.createElement("pre");
        const code = document.createElement("code");
        code.textContent = block.textContent;
        fallback.appendChild(code);
        block.replaceWith(fallback);
      });
      return;
    }

    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: "base",
      themeVariables: {
        background: "#fcfcf9",
        mainBkg: "#fcfcf9",
        primaryColor: "#fcfcf9",
        primaryTextColor: "#181818",
        primaryBorderColor: "#83837e",
        secondaryColor: "#f3f3f4",
        secondaryTextColor: "#222222",
        secondaryBorderColor: "#c1c1c0",
        tertiaryColor: "#efefe4",
        tertiaryTextColor: "#434341",
        tertiaryBorderColor: "#d7d7d6",
        lineColor: "#666666",
        textColor: "#181818",
        edgeLabelBackground: "#fcfcf9",
        clusterBkg: "#efefe4",
        clusterBorder: "#c1c1c0",
        actorBkg: "#fcfcf9",
        actorBorder: "#83837e",
        actorTextColor: "#181818",
        signalColor: "#666666",
        signalTextColor: "#181818",
        noteBkgColor: "#efefe4",
        noteTextColor: "#222222",
        noteBorderColor: "#c1c1c0",
        fontFamily: "Atkinson Hyperlegible Next, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
      },
      flowchart: {
        htmlLabels: true,
        curve: "basis"
      },
      sequence: {
        actorMargin: 48,
        showSequenceNumbers: false
      }
    });

    try {
      await window.mermaid.run({
        nodes: blocks,
        suppressErrors: true
      });
    } catch (error) {
      blocks.forEach((block) => {
        block.classList.add("mermaid-error");
      });
      console.warn("Mermaid rendering failed", error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderMermaid);
  } else {
    renderMermaid();
  }
})();
