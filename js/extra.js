window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

function renderMermaid() {
  if (typeof mermaid === "undefined") return;

  mermaid.initialize({
    startOnLoad: false,
    theme: document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default"
  });

  document.querySelectorAll("pre.mermaid > code").forEach((code) => {
    const pre = code.parentElement;
    pre.textContent = code.textContent;
    pre.classList.add("mermaid");
    pre.removeAttribute("data-processed");
  });

  document.querySelectorAll(".mermaid").forEach((el) => {
    el.removeAttribute("data-processed");
  });

  mermaid.run({ querySelector: ".mermaid" });
}

function renderMathJax() {
  if (typeof MathJax !== "undefined" && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
}

document$.subscribe(() => {
  renderMermaid();
  renderMathJax();
});
