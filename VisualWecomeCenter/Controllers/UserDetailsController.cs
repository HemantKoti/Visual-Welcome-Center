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
using System.Linq;

namespace VisualWelcomeCenter.Controllers
{
    /// <summary>
    /// REST API Controller to do all the required tasks
    /// </summary>
    public class UserDetailsController : Controller
    {
        IEnumerable<UserDetails> userDetails = null;
        ClsMongoDbDataContext _dbContext = new ClsMongoDbDataContext("UserDetails");
        private readonly IHostingEnvironment hostingEnvironment;

        public UserDetailsController(IHostingEnvironment hostingEnvironment)
        {
            this.hostingEnvironment = hostingEnvironment;
        }

        /// <summary>
        /// GET: UserDetails
        /// </summary>
        /// <returns></returns>
        public async Task<ActionResult> Index()
        {
            userDetails = null;
            FilterDefinition<UserDetails> filter = Builders<UserDetails>.Filter.Eq("Name", User.Identity.Name);
            using (IAsyncCursor<UserDetails> cursor = await this._dbContext.GetUserDetails.FindAsync(filter))
            {
                while (await cursor.MoveNextAsync())
                {
                    userDetails = cursor.Current;
                }
            }

            return View(userDetails);
        }

        /// <summary>
        /// GET: UserDetails/Create
        /// </summary>
        /// <returns></returns>
        public ActionResult Create()
        {
            return View();
        }

        // GET: UserDetails/Create
        public ActionResult UpdateProfile()
        {
            return View();
        }

        /// <summary>
        /// POST: UserDetails/Create
        /// </summary>
        /// <param name="model"></param>
        /// <returns></returns>
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

                FilterDefinition<UserDetails> filter = Builders<UserDetails>.Filter.Eq("Name", User.Identity.Name);

                UpdateDefinition<UserDetails> update = Builders<UserDetails>.Update.Set("VisitingPurpose", model.VisitingPurpose);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("AppointmentDate", model.AppointmentDate);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                // await this._dbContext.GetUserDetails.InsertOneAsync(model);

                return RedirectToAction("Index");
            }
            catch (Exception ex)
            {
                return View();
            }
        }

        /// <summary>
        /// POST: UserDetails/UpdateProfile
        /// </summary>
        /// <param name="model"></param>
        /// <returns></returns>
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
                    MemoryStream stream = new MemoryStream();
                    model.Photo.CopyTo(stream);
                    model.Picture = stream.ToArray();
                }

                FilterDefinition<UserDetails> filter = Builders<UserDetails>.Filter.Eq("Name", User.Identity.Name);

                UpdateDefinition<UserDetails> update = Builders<UserDetails>.Update.Set("EmailAddress", model.EmailAddress);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("Picture", model.Picture);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                // await this._dbContext.GetUserDetails.InsertOneAsync(model);

                return RedirectToAction("Index");
            }
            catch (Exception ex)
            {
                return View();
            }
        }
    }
}