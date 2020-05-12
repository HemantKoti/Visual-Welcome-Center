using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataContextLayer;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ModelClass;
using MongoDB.Bson;
using MongoDB.Driver;



namespace CosmosDb_Demo_Crud.Controllers
{
    public class UserDetailsController : Controller
    {
        ClsMongoDbDataContext _dbContext = new ClsMongoDbDataContext("UserDetails");

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

                model.RegisteredDate = DateTime.UtcNow;

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