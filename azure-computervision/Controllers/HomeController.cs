using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using azure_computervision.Models;
using System.IO;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using System.Net.Http;
using System.Net.Http.Headers;
using Newtonsoft.Json.Linq;

namespace azure_computervision.Controllers
{
    public class HomeController : Controller
    {
        private string _azureKey;
        private string _rootFolder;

        public HomeController(IConfiguration iConfig, IHostingEnvironment env) {
             _azureKey = iConfig.GetValue<string>("AzureKey");
             _rootFolder = env.WebRootPath;
        }
        
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost("Upload")]
        public async Task<IActionResult> Upload(IFormFile file)
        {
            // full path to file in temp location
            var filePath = Path.Combine(_rootFolder, $"uploaded/{file.FileName}");

            if (file.Length > 0)
            {
                using (var stream = new FileStream(filePath, FileMode.Create))
                {
                    await file.CopyToAsync(stream);
                }
            }

            var imageResult = JToken.Parse(await ReadHandwrittenText(filePath, _azureKey));
            var imageText = "An error occurred :(";
            if ((string)imageResult["status"] == "Succeeded") {
                imageText = (string)imageResult["recognitionResult"]["lines"][0]["text"];
            }

            // process uploaded files
            ViewBag.ImageUrl = $"/uploaded/{file.FileName}";
            ViewBag.ImageResult = imageText;
            return View("Index");
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }


        /// <summary>
        /// Gets the handwritten text from the specified image file by using
        /// the Computer Vision REST API.
        /// </summary>
        /// <param name="imageFilePath">The image file with handwritten text.</param>
        static async Task<string> ReadHandwrittenText(string imageFilePath, string azureKey)
        {
            try
            {
                HttpClient client = new HttpClient();

                // Request headers.
                client.DefaultRequestHeaders.Add(
                    "Ocp-Apim-Subscription-Key", azureKey);

                // Request parameter.
                // Note: The request parameter changed for APIv2.
                // For APIv1, it is "handwriting=true".
                string requestParameters = "mode=Handwritten";

                // Assemble the URI for the REST API Call.
                string uri = "https://australiaeast.api.cognitive.microsoft.com/vision/v2.0/recognizeText" + "?" + requestParameters;

                HttpResponseMessage response;

                // Two REST API calls are required to extract handwritten text.
                // One call to submit the image for processing, the other call
                // to retrieve the text found in the image.
                // operationLocation stores the REST API location to call to
                // retrieve the text.
                string operationLocation;

                // Request body.
                // Posts a locally stored JPEG image.
                byte[] byteData = GetImageAsByteArray(imageFilePath);

                using (ByteArrayContent content = new ByteArrayContent(byteData))
                {
                    // This example uses content type "application/octet-stream".
                    // The other content types you can use are "application/json"
                    // and "multipart/form-data".
                    content.Headers.ContentType =
                        new MediaTypeHeaderValue("application/octet-stream");

                    // The first REST call starts the async process to analyze the
                    // written text in the image.
                    response = await client.PostAsync(uri, content);
                }

                // The response contains the URI to retrieve the result of the process.
                if (response.IsSuccessStatusCode)
                    operationLocation =
                        response.Headers.GetValues("Operation-Location").FirstOrDefault();
                else
                {
                    // Display the JSON error data.
                    string errorString = await response.Content.ReadAsStringAsync();
                    return errorString;
                }

                // The second REST call retrieves the text written in the image.
                //
                // Note: The response may not be immediately available. Handwriting
                // recognition is an async operation that can take a variable amount
                // of time depending on the length of the handwritten text. You may
                // need to wait or retry this operation.
                //
                // This example checks once per second for ten seconds.
                string contentString;
                int i = 0;
                do
                {
                    System.Threading.Thread.Sleep(1000);
                    response = await client.GetAsync(operationLocation);
                    contentString = await response.Content.ReadAsStringAsync();
                    ++i;
                }
                while (i < 10 && contentString.IndexOf("\"status\":\"Succeeded\"") == -1);

                if (i == 10 && contentString.IndexOf("\"status\":\"Succeeded\"") == -1)
                {
                    return ("{'error':'timeout'}");
                }

                // Display the JSON response.
                return contentString;
            }
            catch (Exception e)
            {
                return e.ToString();
            }
        }

        static byte[] GetImageAsByteArray(string imageFilePath)
        {
            using (FileStream fileStream =
                new FileStream(imageFilePath, FileMode.Open, FileAccess.Read))
            {
                BinaryReader binaryReader = new BinaryReader(fileStream);
                return binaryReader.ReadBytes((int)fileStream.Length);
            }
        }
    }
}
