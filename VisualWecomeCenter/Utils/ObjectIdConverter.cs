using MongoDB.Bson;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Text;

namespace VisualWelcomeCenter.Utils
{
    /// <summary>
    /// Object ID converter
    /// </summary>
    public class ObjectIdConverter : JsonConverter
    {        
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            if (serializer != null & value != null)
            {
                serializer.Serialize(writer, value.ToString());
            }
        }
        
        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            ObjectId objId;
            var token = JToken.Load(reader);
            ObjectId.TryParse(token.ToObject<string>(), out objId);
            return objId;
        }
       
        public override bool CanConvert(Type objectType)
        {
            return objectType == typeof(ObjectId);
        }
    }
}
