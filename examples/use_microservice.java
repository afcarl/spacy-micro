package test;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;

import java.io.IOException;

public class Test {

    /**
     * helper utility to get a json payload from a response object
     * @param response the response object
     * @param clazz the class of the payload
     * @return the de-serialised object of the payload of type clazz
     */
    private static <T> T retrieveResourceFromResponse(HttpResponse response, Class<T> clazz) throws IOException {
        String jsonFromResponse = EntityUtils.toString(response.getEntity());
        ObjectMapper mapper = new ObjectMapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        return mapper.readValue(jsonFromResponse, clazz);
    }

    /**
     * send post
     * @param post post
     * @return the response
     */
    private HttpResponse send(HttpRequestBase post) throws IOException {
        HttpResponse httpResponse = HttpClientBuilder.create()
                    .setSSLHostnameVerifier(NoopHostnameVerifier.INSTANCE)  // ignore invalid hostnames on platform with ssl
                    .build().execute(post);
        if (httpResponse.getStatusLine().getStatusCode() == 200) { // check 200
            return httpResponse;
        }
        return null;
    }

    /**
     * invoke the miro-service to parse the given text and return the json result as text
     * @param text the text to parse
     * @return the response, a string for now - do something more useful with it
     */
    public String parse(String text) throws IOException {
        if ( text != null && text.length() > 0 ) {
            HttpPost post = new HttpPost("http://localhost:9000/parse");

            // set the entity and its mime-type
            StringEntity se = new StringEntity(text);
            se.setContentType(new BasicHeader(HTTP.CONTENT_TYPE, "application/json"));
            post.setEntity(se);

            HttpResponse httpResponse = send(post);
            // Then
            if (httpResponse != null && httpResponse.getStatusLine().getStatusCode() == 200) { // check 200
                return retrieveResourceFromResponse(httpResponse, String.class);
            }
        }
        return null;
    }

}
