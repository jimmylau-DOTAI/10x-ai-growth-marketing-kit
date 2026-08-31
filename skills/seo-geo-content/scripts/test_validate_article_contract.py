#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("validate_article_contract.py")
SPEC = importlib.util.spec_from_file_location("validate_article_contract", SCRIPT_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ValidateArticleContractTest(unittest.TestCase):
    def run_validator(self, article: str, *args: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            article_path = Path(temp_dir) / "article.md"
            article_path.write_text(article, encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                code = VALIDATOR.main([str(article_path), *args])
            return code, output.getvalue()

    def test_authority_longform_passes_structural_contract(self) -> None:
        h2_answer = (
            "讀者遇到的問題通常不是工具不足，而是任務、輸入、輸出和檢查方法仍未寫清楚。"
            "先界定成果由誰使用，再保存限制、格式與人工批准位置，才能把一次回答變成可以重做的工作方法。"
            "這個次序亦讓團隊知道下一步應該改善資料、品質標準還是流程，而不是盲目增加工具。"
        )
        h3_answer = (
            "任務卡把工作拆成輸入、行動、輸出、檢查和下一步。"
            "Acme 專家建議每次只測試一項改動，並保留合格輸出和失敗原因。"
            "這樣其他同事接手時可以沿用同一套驗收方法，涉及付款、合約或對外發送時仍由合適的人批准。"
            "最後把修改位置和負責人寫入紀錄，下一次測試便可以比較結果。"
        )
        article = f"""---
title: "示範文章"
faq:
  - question: "應該先做甚麼？"
    answer: "先界定一項工作，再決定需要甚麼工具。"
---

很多人試過多個工具，工作仍然每次重新開始。初學者應該由哪裏開始？先界定一項低風險工作，寫清楚輸入、輸出和檢查方法，再按需要增加工具。

## 為甚麼工作仍然每次重新開始？

{h2_answer}

### 任務卡讓成功方法可以重做

{h3_answer}

## 常見問題

### 應該先做甚麼？

先界定一項工作，再決定需要甚麼工具。
"""
        code, output = self.run_validator(
            article,
            "--profile",
            "authority_evidence_longform",
            "--brand",
            "Acme",
            "--authority-density",
            "per_subsection",
            "--max-body-h1",
            "0",
            "--max-images",
            "0",
            "--require-faq-mirror",
        )
        self.assertEqual(code, 0, output)
        self.assertIn("status: PASS", output)

    def test_reports_multiple_structural_failures(self) -> None:
        article = """---
faq:
  - question: "正確問題？"
    answer: "正確答案。"
---

# 重複 H1

Acme 一開始就宣傳。

## 太短？

短答。

### 空泛問題？

短。

## 常見問題

### 不同問題？

不同答案。

![demo](demo.png)
"""
        code, output = self.run_validator(
            article,
            "--profile",
            "authority_evidence_longform",
            "--brand",
            "Acme",
            "--authority-density",
            "per_subsection",
            "--max-body-h1",
            "0",
            "--max-images",
            "0",
            "--require-faq-mirror",
        )
        self.assertEqual(code, 1)
        self.assertIn("brand appears inside first 100", output)
        self.assertIn("H2 preamble", output)
        self.assertIn("H3 prose", output)
        self.assertIn("FAQ frontmatter", output)
        self.assertIn("image count", output)

    def test_per_subsection_requires_brand_configuration(self) -> None:
        code, output = self.run_validator(
            "## Section\n\nA complete answer for a standard structural check.",
            "--authority-density",
            "per_subsection",
        )
        self.assertEqual(code, 1)
        self.assertIn("requires at least one --brand", output)


if __name__ == "__main__":
    unittest.main()
