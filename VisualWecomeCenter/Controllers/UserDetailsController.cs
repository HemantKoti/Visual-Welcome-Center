using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Bson;
using MongoDB.Driver;
using VisualWelcomeCenter.Models;
using VisualWelcomeCenter.Utils;
using Microsoft.AspNetCore.Identity;
using System.IO;
using Microsoft.AspNetCore.Hosting;

namespace VisualWelcomeCenter.Controllers
{
    public class UserDetailsController : Controller
    {
        ClsMongoDbDataContext _dbContext = new ClsMongoDbDataContext("UserDetails");
        private readonly IHostingEnvironment hostingEnvironment;

        public UserDetailsController(IHostingEnvironment hostingEnvironment)
        {
            this.hostingEnvironment = hostingEnvironment;
        }


        // GET: UserDetails
        public async Task<ActionResult> Index()
        {
            IEnumerable<UserDetails> userDetails = null;
            using (IAsyncCursor<UserDetails> cursor = await this._dbContext.GetUserDetails.FindAsync(new BsonDocument()))
            {
                while (await cursor.MoveNextAsync())
                {
                    userDetails = cursor.Current;
                }
            }

            return View(userDetails);
        }

        // GET: UserDetails/Create
        public ActionResult Create()
        {
            return View();
        }

        // GET: UserDetails/Create
        public ActionResult UpdateProfile()
        {
            return View();
        }

        // POST: UserDetails/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> Create(UserDetails model)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    return View(model);
                }

                model.Name = User.Identity.Name;
                model.LastEnteredDate = DateTime.UtcNow;

                await this._dbContext.GetUserDetails.InsertOneAsync(model);

                return RedirectToAction("Index");
            }
            catch
            {
                return View();
            }
        }

        // POST: UserDetails/UpdateProfile
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> UpdateProfile(UserDetails model)
        {
            try
            {
                string uniqueFileName = null;

                if (!ModelState.IsValid)
                {
                    return View(model);
                }

                if (model.Photo != null)
                {
                    string uploadsFolder = Path.Combine(hostingEnvironment.WebRootPath, "images");

                    uniqueFileName = Guid.NewGuid().ToString() + "_" + model.Photo.FileName;
                    string filePath = Path.Combine(uploadsFolder, uniqueFileName);

                    FileStream image = new FileStream(filePath, FileMode.Create);
                    model.Photo.CopyTo(image);
                }

                model.Name = User.Identity.Name;
                model.LastEnteredDate = DateTime.UtcNow;

                await this._dbContext.GetUserDetails.InsertOneAsync(model);

                return RedirectToAction("Index");
            }
            catch
            {
                return View();
            }
        }
    }
}