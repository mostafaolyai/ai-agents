```
from pydantic import BaseModel

class GaiaOutput(BaseModel):
  is_solvable: bool
  unsolvable_reason: str = ""
  final_answer: str = ""

```

* `is_solvable`: مدل ابتدا باید بگوید آیا بدون امکانات بیرونی قادر به حل این مسئله است یا خیر[36].
* `unsolvable_reason`: اگر قادر نیست (`False`)، دلیل آن را ثبت کند (مثلاً «من به اینترنت دسترسی ندارم»)[36].
* `final_answer`: اگر می‌تواند (`True`)، پاسخ عددی یا متنی نهایی خود را قرار دهد[36][37].

===
```
import asyncio

PROVIDER_SEMAPHORES = {
    "openai": asyncio.Semaphore(30),
    "anthropic": asyncio.Semaphore(10),
    "gemini": asyncio.Semaphore(10),
}

def get_provider(model: str) ->: str:
  """تشخیص ارائه‌دهنده بر اساس پیشوند نام مدل"""
  return "anthropic" if model.startswith("anthropic/") else "openai"

```
========

```
from litellm import acompletion

gaia_prompt = """You are a general AI assistant. I will ask you a question.
First, determine if you can solve this problem with your current capabilities and set "is_solvable" accordingly.
If you can solve it, set "is_solvable" to true and provide your answer in "final_answer".
If you cannot solve it, set "is_solvable" to false and explain why in "unsolvable_reason".
Your final answer should be a number OR as few words as possible OR a comma-separated list of numbers and/or strings.
"""

async def solve_problem(model: str, question: str) ->: GaiaOutput:
  """حل یک مسئله مستقل با کنترل نرخ و بازگشت خروجی ساختاریافته"""
  provider = get_provider(model)
  async with PROVIDER_SEMAPHORES[provider]:
    response = await acompletion(
        model=model,
        messages=[
            {"role": "system", "content": gaia_prompt},
            {"role": "user", "content": question},
        ],
        response_format=GaiaOutput,
        num_retries=2,
    )
    finish_reason = response.choices.finish_reason
    content = response.choices.message.content

    # مدیریت حالتی که مدل از پاسخ به خاطر مسایل ایمنی امتناع می‌کند
    if finish_reason == "refusal" or content is None:
      return GaiaOutput(
          is_solvable=False,
          unsolvable_reason=(
              f"Model refused to answer (finish_reason: {finish_reason})"
          ),
          final_answer="",
      )
    return GaiaOutput.model_validate_json(content)

```
=========
#### کد ۲.۱۴ و ۲.۱۵: مقایسه پاسخ با Ground Truth و تجمیع فراداده‌ها[41][42]
```
def is_correct(prediction: str | None, answer: str) ->: bool:
  """بررسی برابری دقیق پاسخ بدون در نظر گرفتن فاصله خالی و بزرگی/کوچکی حروف"""
  if prediction is None:
    return False
  return prediction.strip().lower() == answer.strip().lower()

async def evaluate_gaia_single(problem: dict, model: str) ->: dict:
  """ارزیابی یک مسئله روی یک مدل مشخص و ثبت گزارش کامل"""
  try:
    output = await solve_problem(model, problem["Question"])
    return {
      "task_id": problem["task_id"],
      "model": model,
      "correct": is_correct(output.final_answer, problem["Final answer"]),
      "is_solvable": output.is_solvable,
      "prediction": output.final_answer,
      "answer": problem["Final answer"],
      "unsolvable_reason": output.unsolvable_reason,
    }
  except Exception as e:
    return {
      "task_id": problem["task_id"],
      "model": model,
      "correct": False,
      "is_solvable": None,
      "prediction": None,
      "answer": problem["Final answer"],
      "error": str(e),
    }

```

---
