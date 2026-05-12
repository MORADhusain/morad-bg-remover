from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import json
import os

app = FastAPI()

# ডাটা লোড করার ফাংশন
def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

@app.get("/")
def health_check():
    return {"status": "Online", "owner": "Md. Murad Hasan", "message": "API is running successfully"}

@app.post("/remove")
async def remove_bg(image: UploadFile = File(...), user_id: str = None):
    # ইউজার আইডি চেক করা (যদি আপনি সিকিউরিটি রাখতে চান)
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    try:
        # ছবি পড়া
        input_image = await image.read()
        
        # ব্যাকগ্রাউন্ড রিমুভ করা
        output_image = remove(input_image)
        
        # আউটপুট ইমেজ স্ট্রিমিং রেসপন্স হিসেবে পাঠানো
        return StreamingResponse(io.BytesIO(output_image), media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
