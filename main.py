from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# ────── تابع‌های کمکی ──────

def default_headers():
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en"
    }

def parse_cookie(response):
    cookies = response.headers.get("set-cookie", "")
    cookies = "; ".join([x.split(";")[0] for x in cookies.split(",")])
    return cookies

def get_result(task_id, cookies, tries=1):
    url = f"https://videoplus.ai/veo2/api/text-to-video/get-task-result?task_id={task_id}"
    headers = {
        **default_headers(),
        "cookie": cookies
    }
    try:
        r = requests.get(url, headers=headers)
        data = r.json().get("data", {})
        status = data.get("status", 0)
        if status == 0:
            if tries > 25:
                return "Error!"
            time.sleep(3)
            return get_result(task_id, cookies, tries + 1)
        elif status == 1:
            return data.get("task_result", {}).get("result", [{}])[0].get("video_path", "Error!")
        else:
            return "Error!"
    except Exception as e:
        print("get_result error:", e)
        return "Error!"

def text_to_video_v1(p=""):
    try:
        optimize_url = "https://videoplus.ai/veo2/api/prompt/optimize"
        headers1 = {
            **default_headers(),
            "cookie": "NUXT_LOCALE=en",
            "content-type": "application/json"
        }
        payload1 = {
            "customer_prompt": p,
            "prompt_type": "vidu"
        }
        r1 = requests.post(optimize_url, json=payload1, headers=headers1)
        data1 = r1.json().get("data", {})
        optimized_prompt = data1.get("ai_result", p)
        cookies = "NUXT_LOCALE=en; " + parse_cookie(r1)
    except Exception as e:
        print("optimize error:", e)
        return "Error!"

    try:
        create_url = "https://videoplus.ai/veo2/api/text-to-video/create-task"
        headers2 = {
            **default_headers(),
            "cookie": cookies,
            "content-type": "application/json"
        }
        payload2 = {
            "prompt_text": optimized_prompt,
            "style": "general",
            "resolution": "512",
            "movement_amplitude": "auto",
            "duration": 4,
            "task_type": 1
        }
        r2 = requests.post(create_url, json=payload2, headers=headers2)
        data2 = r2.json().get("data", {})
        task_id = data2.get("task_id", "")
        if task_id:
            return get_result(task_id, cookies)
        else:
            print("create-task error: No task_id found.")
            return "Error!"
    except Exception as e:
        print("create-task error:", e)
        return "Error!"

# ────── روت اصلی وب‌سرویس ──────

@app.get("/generate-video")
async def generate_video(prompt: str = ""):
    if not prompt:
        return JSONResponse(content={
            "success": False,
            "link": "error",
            "by": "https://t.me/Afshin_Sukuna",
            "channel": "https://t.me/Starless_Soull"
        })

    result = text_to_video_v1(prompt)
    is_success = result != "Error!"

    return JSONResponse(content={
        "success": is_success,
        "link": result if is_success else "error",
        "by": "https://t.me/Afshin_Sukuna",
        "channel": "https://t.me/Starless_Soull"
    })
