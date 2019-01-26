from PIL import Image, ImageFont, ImageDraw
import io
import aiohttp
import json
import os

class ImageProcessing:
    async def PIL_image_from_url(url):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            uimg = io.BytesIO()
            uimg.write(await resp.read())
            return Image.open(uimg)
    
    async def image_from_url(url):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            uimg = io.BytesIO()
            uimg.write(await resp.read())
            return uimg

class config:
    def get(a):
        try:
            return os.environ[a]
        except IndexError:
            with open("config.txt", "r") as f:
                j = json.loads(f.read())
                return j[a]