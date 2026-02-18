import asyncio
from services.video_repair.get_failed_video_service import get_failed_videos
from services.video_repair.video_repair_worker import repair_video

async def auto_repair_loop():
    """
        Auto-repairs failed videos every 30 minutes in background.
    """
    while True:
        try:
            failed_video_ids = await asyncio.to_thread(get_failed_videos, limit = 5)

            if failed_video_ids:
                print("Failed videos -> repairing....")

                # Create repair tasks for each failed video
                tasks = []
                for video_id, languages in failed_video_ids:
                    tasks.append(asyncio.create_task(repair_video(video_id, languages)))

                # Run all repairs in parallel (don’t stop if any fails)
                results = await asyncio.gather(*tasks, return_exceptions = True)

                # Log only the videos whose repair failed
                for index, item in enumerate(results):
                    video_id = failed_video_ids[index] [0]

                    if isinstance(item, Exception):
                        print(f"Repair failed for video ID {video_id}: {item}")
                
                print("repair batch complete")

            else:
                print("No FAILED videos found")

        except Exception as e:
            print(f"Auto repair scheduler crashed: {e}")   

        await asyncio.sleep(1800)
               