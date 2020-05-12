using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ModelClass
{
    public class UserDetails
    {
        public UserDetails()
        {
            RegisteredDate = DateTime.Now;
        }

        [BsonId]
        [JsonProperty("objectId"), JsonConverter(typeof(ObjectIdConverter))]
        public ObjectId ObjectId { get; set; }

        [Key]
        public int UserDetailsId { get; set; }

        [Required(ErrorMessage = "Please Enter your Name")]
        [Column(TypeName = "varchar(50)")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Please Enter your Email Address")]
        [Column(TypeName = "varchar(50)")]
        public string EmailAddress { get; set; }

        [Column(TypeName = "varchar(50)")]
        public string PhoneNumber { get; set; }

        [Required(ErrorMessage = "Please Enter your Purpose of Visit")]
        [Column(TypeName = "varchar(500)")]
        public string VisitingPurpose { get; set; }

        [Column(TypeName = "varchar(50)")]
        public string ImageName { get; set; }

        [Column(TypeName = "varchar(250)")]
        public string ImagePath { get; set; }
        
        public DateTime RegisteredDate { get; set; }

        public DateTime? LastEnteredDate { get; set; }
    }
}
