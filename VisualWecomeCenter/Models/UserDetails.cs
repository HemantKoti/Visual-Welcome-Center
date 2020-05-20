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
    /// <summary>
    /// User Details model class
    /// </summary>
    public class UserDetails
    {
        public UserDetails()
        {
            AppointmentDate = DateTime.Now;
        }

        [BsonId]
        [JsonProperty("objectId"), JsonConverter(typeof(ObjectIdConverter))]
        public ObjectId ObjectId { get; set; }

        [Key]
        [BsonElement("EmailAddress")]
        [Column(TypeName = "varchar(50)")]
        [DataType(DataType.EmailAddress)]
        [Required]
        public string EmailAddress { get; set; }

        [BsonElement("Name")]
        [Column(TypeName = "varchar(50)")]
        [Required]
        public string Name { get; set; }

        [BsonElement("JobTitle")]
        [Column(TypeName = "varchar(50)")]
        public string JobTitle { get; set; }

        [BsonElement("VisitingPurpose")]
        [Column(TypeName = "varchar(200)")]
        [DataType(DataType.MultilineText)]
        public string VisitingPurpose { get; set; }

        [BsonElement("AppointmentDate")]
        [Column(TypeName = "date")]
        [DataType(DataType.DateTime)]
        public DateTime? AppointmentDate { get; set; }

        [BsonElement("LastLogin")]
        [Column(TypeName = "varchar(50)")]
        public string LastLogin { get; set; }

        [BsonElement("Picture")]
        [Column(TypeName = "array")]
        public byte[] Picture { get; set; }

        [BsonElement("Encodings")]
        [Column(TypeName = "array")]
        public byte[] Encodings { get; set; }

        [DataType(DataType.Upload)]
        public IFormFile Photo { get; set; }
    }
}
