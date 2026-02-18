import express from "express";
import { extractVideoId } from "../utils/youtubeUrl.utils.js";
import { detectVideoLanguage } from "../utils/languageDetection.utils.js"
import axios from "axios"

const router = express.Router()

// send data to query route in python
router.post('/query', async(req, res) => {
    const { youtubeUrl, question } = req.body

    try {
        if(!youtubeUrl){
        return res.status(400).json({
            message : "youtube URL required"
        })
    }

    if (!question){
        return res.status(400).json({
            message : "Query is required"
        })
    }

    //fetch videoID
    const videoId = extractVideoId(youtubeUrl)

    //Language detection
    const languages = await detectVideoLanguage(videoId)

    const pythonResponse = await axios.post("http://localhost:8000/query", {
        videoId,
        question,
        languages
    })

    return res.json({
        message : "Data sent to query route successfully",
        pythonResponse : pythonResponse.data
    })
    }

    catch(error){
        console.log(error)
        return res.status(500).json({
            error : "Failed to send the videoId to python"
        })
    }   
})

export default router