import axios from "axios"

export async function detectVideoLanguage(videoId){
    try {
        const ytHTMLPage = await axios.get(
            `https://www.youtube.com/watch?v=${videoId}`
        )

        const html = ytHTMLPage.data
        
        let languages = "en"
        
        const captureLanguage = html.match(/"languageCode":"(.*?)"/)

        if(captureLanguage && captureLanguage[1]){
            return languages = captureLanguage[1];
        }
    }

    catch(e) {
        console.error("Language detection failed:", e);
        return "en";
    }
}