import express from "express"
import queryRoutes from "./routes/query.route.js";

const app = express()

app.use(express.json())

app.use("/api/v1/youtube", queryRoutes);

app.listen(3000, () => {
    console.log(`App is listening on port 3000`);  
})