using MongoDB.Driver;
using VisualWelcomeCenter.Models;

namespace VisualWelcomeCenter.Utils
{
    /// <summary>
    /// Mongo DB connector class
    /// </summary>
    public class ClsMongoDbDataContext
    {
        private string _connectionStrings = string.Empty;
        private string _databaseName = string.Empty;
        private string _collectionName = string.Empty;

        public ClsMongoDbDataContext(string strCollectionName)
        {
            this._collectionName = strCollectionName;
            this._connectionStrings = AppConfiguration.GetConfiguration("ServerName");
            this._databaseName = AppConfiguration.GetConfiguration("DatabaseName");
            this.Client = new MongoClient(_connectionStrings);
            this.Database = Client.GetDatabase(_databaseName);
        }

        public IMongoClient Client { get; }

        public IMongoDatabase Database { get; }

        public IMongoCollection<UserDetails> GetUserDetails
        {
            get { return Database.GetCollection<UserDetails>(_collectionName); }
        }
    }
}
