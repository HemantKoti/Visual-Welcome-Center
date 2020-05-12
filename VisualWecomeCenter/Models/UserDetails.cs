using Microsoft.AspNetCore.Http;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using VisualWelcomeCenter.Utils;

namespace VisualWelcomeCenter.Models
{
    public class UserDetails
    {
        public UserDetails()
        {
            LastEnteredDate = DateTime.Now;
        }

        [BsonId]
        [JsonProperty("objectId"), JsonConverter(typeof(ObjectIdConverter))]
        public ObjectId ObjectId { get; set; }

        [Key]
        [BsonElement]
        // [Required(ErrorMessage = "Please Enter your Name")]
        [Column(TypeName = "varchar(50)")]
        public string Name { get; set; }

        [BsonElement]
        // [Required(ErrorMessage = "Please Enter your Email Address")]
        [Column(TypeName = "varchar(50)")]
        public string EmailAddress
        {
            get; set;
        }

        [BsonElement]
        // [Required(ErrorMessage = "Please Enter your Purpose of Visit")]
        [Column(TypeName = "varchar(500)")]
        public string VisitingPurpose { get; set; }

        [BsonElement]
        [Column(TypeName = "varchar(50)")]
        public string ImageName { get; set; }

        [BsonElement]
        public IFormFile Photo { get; set; }

        [BsonElement]
        [DataType(DataType.DateTime)]
        public DateTime? LastEnteredDate { get; set; }
    }
}
