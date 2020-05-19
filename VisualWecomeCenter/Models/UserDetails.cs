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
        [BsonElement("Name")]
        [Column(TypeName = "varchar(50)")]
        public string Name { get; set; }

        [BsonElement("EmailAddress")]
        [Column(TypeName = "varchar(50)")]
        [DataType(DataType.EmailAddress)]
        public string EmailAddress { get; set; }

        [BsonElement("VisitingPurpose")]
        public string VisitingPurpose { get; set; }

        public IFormFile Photo { get; set; }

        [BsonElement("AppointmentDate")]
        [Column(TypeName = "date")]
        [DataType(DataType.DateTime)]
        public DateTime? AppointmentDate { get; set; }

        [BsonElement("LastEntered")]
        [DataType(DataType.DateTime)]
        [Column(TypeName = "date")]
        public DateTime? LastEntered { get; set; }

        [BsonElement("Picture")]
        [Column(TypeName = "array")]
        public byte[] Picture { get; set; }

        [BsonElement("Encodings")]
        [Column(TypeName = "array")]
        public byte[] Encodings { get; set; }
    }
}
