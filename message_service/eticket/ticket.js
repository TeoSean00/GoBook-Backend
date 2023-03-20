const QRCode = require('qrcode');
// const mustache = require('mustache');
const logger = require("../utils/logger");
const { getLogger } = require("nodemailer/lib/shared/index.js");

const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const hbs = require ('handlebars');
const path = require('path');

// compile the hbs template to pdf template
const compile = async function (templateName, data) {
    const filePath = path.join(process.cwd(), 'templates', `${templateName}.hbs`);

    // get the html 
    const html = await fs.readFile(filePath, 'utf-8');

    return hbs.compile(html)(data);
};


async function createPDF(dataObject) {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        const content = await compile('index', dataObject);

        await page.setContent(content);
        
        // create a pdf document
        await page.pdf({
            path: 'eticket.pdf',
            // format: 'A4',
            printBackground: false,

        })
        logger.info("done creating pdf");
        await browser.close();
        process.exit()
    }
    catch (e) {
        console.log(e);
    }
}

module.exports = createPDF;
