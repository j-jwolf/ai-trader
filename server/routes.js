const router = require("express").Router();
const cheerio = require("cheerio");
const request = require("request");

const yahoo = "https://finance.yahoo.com/quote/";
const historicalData = "/history?p=";

router.get("/historicalData/:stock", (req, res) => {
    console.log(`new connection --> stock: ${req.params.stock}`);
    // initialize variables
    let data = {
        status: "",
        content: {
            message: "",
            data: []
        }
    };
    let url = yahoo+req.params.stock+historicalData+req.params.stock;

    // make request to yahoo finance
    request(url, (err, response, html) => {
        if(!err && response.statusCode === 200)
        {
            // scrape html
            let $ = cheerio.load(html);
            $("table tbody tr").each((i, row) => {
                let temp = {
                    date: $(row).find("td:first-child span").text(),
                    open: $(row).find("td:nth-child(2)").text(),
                    high: $(row).find("td:nth-child(3)").text(),
                    low: $(row).find("td:nth-child(4)").text(),
                    close: $(row).find("td:nth-child(5)").text()
                }
                // add json to response data
                data.content.data.push(temp);
            });
            
            // set status to ok
            data.status = "OK";
            
            // give message
            data.content.message = "Retrieved historical data for "+req.params.stock;

            // set status code and send data back
            res.status(200).json(data);
        }
        else
        {
            console.log(`error scraping for ${req.params.stock}`);
            // send 500 error with json describing error
            res.status(500).json({
                status: "ERROR",
                content: {
                    message: "Failed to scrape "+req.params.stock,
                    data: []
                }
            });
        }
    });
});

// export
module.exports = router;