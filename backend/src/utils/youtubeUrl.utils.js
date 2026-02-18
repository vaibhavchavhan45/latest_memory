export function extractVideoId(ytUrl){
    try {
        const url = new URL(ytUrl)

        const hostname = url.hostname.replace("www.", "")

        //Allow the yt hosts only
        const allowedHosts = ["youtube.com", "youtu.be", "m.youtube.com"]
        if(!allowedHosts.some((host) => hostname.includes(host))){
            return null
        }

        //e.g. youtu.be/VIDEOID
        if(hostname === "youtu.be"){
            const videoId = url.pathname.slice(1)
            return videoId || null
        }

        //e.g. youtube.com/watch?v=VIDEOID
        if(url.pathname === '/watch'){
            const videoId = url.searchParams.get("v") 
            return videoId || null
        }

        //e.g. youtube.com/shorts/VIDEOID
        if(url.pathname.startsWith('/shorts/')){
            const videoId = url.pathname.split('/shorts/')[1]
            return videoId || null
        }

        //e.g.  youtube.com/embed/VIDEOID
        if(url.pathname.startsWith('/embed/')){
            const videoId = url.pathname.split('/embed/')[1]
            return videoId || null
        }

        return null
    } 
    
    catch (error) {
        console.log("Wrong youtube URL", error)
    }
}