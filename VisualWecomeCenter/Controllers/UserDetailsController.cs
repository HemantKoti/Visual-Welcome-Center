using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using VisualWelcomeCenter.Models;
using VisualWelcomeCenter.Utils;
using System.IO;
using Microsoft.AspNetCore.Hosting;
using DnsClient.Internal;
using Microsoft.Extensions.Logging;
using System.Security.Claims;
using System.Linq;
using Microsoft.AspNetCore.Http;

namespace VisualWelcomeCenter.Controllers
{
    /// <summary>
    /// REST API Controller to do all the required tasks
    /// </summary>
    [Microsoft.AspNetCore.Authorization.Authorize]
    public class UserDetailsController : Controller
    {
        IEnumerable<UserDetails> userDetails = null;
        ClsMongoDbDataContext _dbContext = new ClsMongoDbDataContext("UserDetails");
        readonly string emailAddress = string.Empty;

        [Obsolete]
        public IHostingEnvironment HostingEnvironment { get; }

        public Microsoft.Extensions.Logging.ILogger<UserDetailsController> Logger { get; }

        [Obsolete]
        public UserDetailsController(IHostingEnvironment hostingEnvironment, ILogger<UserDetailsController> logger, IHttpContextAccessor httpContextAccessor)
        {
            this.HostingEnvironment = hostingEnvironment;
            this.Logger = logger;

            var identity = httpContextAccessor.HttpContext.User.Identity as ClaimsIdentity;
            this.emailAddress = identity.Claims.FirstOrDefault(x => x.Type == "emails")?.Value;
        }

        /// <summary>
        /// GET: UserDetails
        /// </summary>
        /// <returns></returns>
        public async Task<ActionResult> Index()
        {
            this.Logger.LogInformation("Enter Index()");

            userDetails = null;
            FilterDefinition<UserDetails> filter = Builders<UserDetails>.Filter.Eq("EmailAddress", this.emailAddress);
            using (IAsyncCursor<UserDetails> cursor = await this._dbContext.GetUserDetails.FindAsync(filter))
            {
                while (await cursor.MoveNextAsync())
                {
                    userDetails = cursor.Current;
                }
            }

            this.Logger.LogInformation("Exit Index()");
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
            this.Logger.LogInformation("Enter Create Schedule()");

            try
            {
                if (!ModelState.IsValid)
                {
                    return View(model);
                }

                FilterDefinition<UserDetails> filter = Builders<UserDetails>.Filter.Eq("EmailAddress", this.emailAddress);

                UpdateDefinition<UserDetails> update = Builders<UserDetails>.Update.Set("Name", model.Name);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("JobTitle", model.JobTitle);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("VisitingPurpose", model.VisitingPurpose);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("AppointmentDate", model.AppointmentDate);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                this.Logger.LogInformation("Exit Create Schedule()");
                return RedirectToAction("Index");
            }
            catch (Exception ex)
            {
                this.Logger.LogError("Create Schedule() Exception: " + ex.ToString());
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
            this.Logger.LogInformation("Enter UpdateProfile()");

            try
            {
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

                FilterDefinition<UserDetails> filter = Builders<UserDetails>.Filter.Eq("EmailAddress", this.emailAddress);

                UpdateDefinition<UserDetails> update = Builders<UserDetails>.Update.Set("Name", model.Name);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("JobTitle", model.JobTitle);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                update = Builders<UserDetails>.Update.Set("Picture", model.Picture);
                await this._dbContext.GetUserDetails.UpdateOneAsync(filter, update, new UpdateOptions() { IsUpsert = true });

                this.Logger.LogInformation("Exit UpdateProfile()");
                return RedirectToAction("Index");
            }
            catch (Exception ex)
            {
                this.Logger.LogError("UpdateProfile Exception: " + ex.ToString());
                return View();
            }
        }
    }
}