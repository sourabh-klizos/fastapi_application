from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from app.database.db import get_db
from pymongo.collection import Collection



async def delete_users_from_trash():
    async for db in get_db():

        trash_collection :Collection =  db['trash']
        threshold_date = datetime.now() - timedelta(days=30)
        await trash_collection.delete_many({"deleted_at" :{"$lt" :threshold_date }})

scheduler = AsyncIOScheduler()
scheduler.add_job(delete_users_from_trash, IntervalTrigger(days=1)) 