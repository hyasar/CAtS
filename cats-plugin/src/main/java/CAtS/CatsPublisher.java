package CAtS;

import hudson.Launcher;
import hudson.Extension;
import hudson.tasks.*;
import hudson.util.FormValidation;
import hudson.model.AbstractBuild;
import hudson.model.BuildListener;
import hudson.model.AbstractProject;
import net.sf.json.JSONObject;
import org.apache.commons.io.filefilter.RegexFileFilter;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.stapler.StaplerRequest;
import org.kohsuke.stapler.QueryParameter;

import javax.servlet.ServletException;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.file.Files;

/**
 * Sample {@link Builder}.
 *
 * <p>
 * When the user configures the project and enables this builder,
 * {@link DescriptorImpl#newInstance(StaplerRequest)} is invoked
 * and a new {@link CatsPublisher} is created. The created
 * instance is persisted to the project configuration XML by using
 * XStream, so this allows you to use instance fields (like {@link #projectId})
 * to remember the configuration.
 *
 * <p>
 * When a build is performed, the {@link #perform(AbstractBuild, Launcher, BuildListener)}
 * method will be invoked.
 */

public class CatsPublisher extends Recorder {

    private final String username;
    private final String password;
    private final String projectId;
    private final String outputDir;


    // Fields in config.jelly must match the parameter names in the "DataBoundConstructor"
    @DataBoundConstructor
    public CatsPublisher(String username, String password, String projectId, String outputDir) {
        this.username = username;
        this.password = password;
        this.projectId = projectId;
        this.outputDir = outputDir;
    }

    /**
     * We'll use this from the <tt>config.jelly</tt>.
     */
    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getProjectId() {
        return projectId;
    }

    public String getOutputDir() {
        return outputDir;
    }

    @Override
    public boolean perform(AbstractBuild build, Launcher launcher, BuildListener listener) throws IOException {
        // This is where you 'build' the project.
        // Here we will retrieve the testing report

        // This also shows how you can consult the global configuration of the builder
        String casUrl = getDescriptor().getCasUrl();
        String casPort = getDescriptor().getCasPort();
        if (casUrl != null)
            listener.getLogger().println("CAS Host Url is " + casUrl + "!");
        listener.getLogger().println("Project id is " + projectId + "!");


        listener.getLogger().println("[Build Dir]" + build.getWorkspace());
        listener.getLogger().println("[Print file list] for build #" + build.getNumber());


        final int buildNumber = build.getNumber();
        String workspace = build.getWorkspace() + "/" + outputDir;

        File dir = new File(workspace);
        String pattern = "Assessment.*build-" + buildNumber + ".*.xml";
        FileFilter filter = new RegexFileFilter(pattern);
        File[] files = dir.listFiles(filter);


        if (files == null)
            return true;

        for (File file : files) {
            listener.getLogger().println(file);
        }

//        Call API of Cas web service to receive testing reports
        String url = "http://" + casUrl + ":" + casPort + "/parse_report";
        listener.getLogger().println("[Send to]" + url);

        String charset = "UTF-8";

        File firstFile = files[0];
        String boundary = Long.toHexString(System.currentTimeMillis()); // Just generate some unique random value.
        String crlf = "\r\n"; // Line separator required by multipart/form-data.

        HttpURLConnection connection = (HttpURLConnection)new URL(url).openConnection();
        connection.setDoOutput(true);
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

        OutputStream output = connection.getOutputStream();
        String contentTypeString = "Content-Type: text/plain; charset=";

        output.write(("--"+boundary+crlf).getBytes());
        output.write("Content-Disposition: form-data; name=\"username\"\r\n".getBytes());
        output.write((contentTypeString + charset+crlf).getBytes());
        output.write((crlf+username+crlf).getBytes());

        output.write(("--"+boundary+crlf).getBytes());
        output.write("Content-Disposition: form-data; name=\"password\"\r\n".getBytes());
        output.write((contentTypeString + charset+crlf).getBytes());
        output.write((crlf+password+crlf).getBytes());

        output.write(("--"+boundary+crlf).getBytes());
        output.write("Content-Disposition: form-data; name=\"projectId\"\r\n".getBytes());
        output.write((contentTypeString + charset+crlf).getBytes());
        output.write((crlf+projectId+crlf).getBytes());

        output.write(("--"+boundary+crlf).getBytes());
        output.write("Content-Disposition: form-data; name=\"buildNumber\"\r\n".getBytes());
        output.write((contentTypeString + charset+crlf).getBytes());
        output.write((crlf+String.valueOf(buildNumber)+crlf).getBytes());

        output.write(("--"+boundary+crlf).getBytes());
        output.write("Content-Disposition: form-data; name=\"testingReport\"\r\n".getBytes());
        output.write((contentTypeString + charset+crlf).getBytes());
        output.write((crlf).getBytes());
        Files.copy(firstFile.toPath(), output);
        output.write((crlf).getBytes());
        output.flush();
        output.close();

        int responseCode = connection.getResponseCode();
        listener.getLogger().println("POST Response Code ::  " + responseCode);
        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            listener.getLogger().println(response.toString());
        } else {
            listener.getLogger().println("POST request not worked");
        }

        /*
        try (
                OutputStream output = connection.getOutputStream();
                PrintWriter writer = new PrintWriter(new OutputStreamWriter(output, charset), true);
        ) {
            // Send normal param.
            String contentTypeString = "Content-Type: text/plain; charset=";

            writer.append("--" + boundary).append(crlf);
            writer.append("Content-Disposition: form-data; name=\"username\"").append(crlf);
            writer.append(contentTypeString + charset).append(crlf);
            writer.append(crlf).append(username).append(crlf).flush();

            writer.append("--" + boundary).append(crlf);
            writer.append("Content-Disposition: form-data; name=\"password\"").append(crlf);
            writer.append(contentTypeString + charset).append(crlf);
            writer.append(crlf).append(password).append(crlf).flush();

            writer.append("--" + boundary).append(crlf);
            writer.append("Content-Disposition: form-data; name=\"projectId\"").append(crlf);
            writer.append(contentTypeString + charset).append(crlf);
            writer.append(crlf).append(projectId).append(crlf).flush();

            writer.append("--" + boundary).append(crlf);
            writer.append("Content-Disposition: form-data; name=\"buildNumber\"").append(crlf);
            writer.append(contentTypeString + charset).append(crlf);
            writer.append(crlf).append(String.valueOf(buildNumber)).append(crlf).flush();

            // Send text file.
            writer.append("--" + boundary).append(crlf);
            writer.append("Content-Disposition: form-data; name=\"testingReport\"; filename=\"" + firstFile.getName() + "\"").append(crlf);
            writer.append(contentTypeString + charset).append(crlf); // Text file itself must be saved in this charset!
            writer.append(crlf).flush();
            Files.copy(firstFile.toPath(), output);
            output.flush(); // Important before continuing with writer!
            writer.append(crlf).flush(); // crlf is important! It indicates end of boundary.


            writer.append("--" + boundary + "--").append(crlf).flush();
        }
        */
        return true;
    }

    // Overridden for better type safety.
    // If your plugin doesn't really define any property on Descriptor,
    // you don't have to do this.
    @Override
    public DescriptorImpl getDescriptor() {
        return (DescriptorImpl) super.getDescriptor();
    }

    public BuildStepMonitor getRequiredMonitorService() {
        return BuildStepMonitor.NONE;
    }

    /**
     * Descriptor for {@link CatsPublisher}. Used as a singleton.
     * The class is marked as public so that it can be accessed from views.
     *
     * <p>
     * See <tt>src/main/resources/hudson/plugins/hello_world/CatsPublisher/*.jelly</tt>
     * for the actual HTML fragment for the configuration screen.
     */
    @Extension // This indicates to Jenkins that this is an implementation of an extension point.
    public static final class DescriptorImpl extends BuildStepDescriptor<Publisher> {
        /**
         * To persist global configuration information,
         * simply store it in a field and call save().
         *
         * <p>
         * If you don't want fields to be persisted, use <tt>transient</tt>.
         */

        private String casUrl;
        private String casPort;

        /**
         * Performs on-the-fly validation of the form field 'name'.
         *
         * @param value This parameter receives the value that the user has typed.
         * @return Indicates the outcome of the validation. This is sent to the browser.
         */
        public FormValidation doCheckName(@QueryParameter String value)
                throws IOException, ServletException {
            if (value.length() == 0)
                return FormValidation.error("Please set a name");
            if (value.length() < 4)
                return FormValidation.warning("Isn't the name too short?");
            return FormValidation.ok();
        }

        public boolean isApplicable(Class<? extends AbstractProject> aClass) {
            // Indicates that this builder can be used with all kinds of project types 
            return true;
        }

        /**
         * This human readable name is used in the configuration screen.
         */
        public String getDisplayName() {
            return "Send Testing Report to CAS";
        }

        @Override
        public boolean configure(StaplerRequest req, JSONObject formData) throws FormException {
            // To persist global configuration information,
            // set that to properties and call save().
            casUrl = formData.getString("casUrl");
            casPort = formData.getString("casPort");
            save();
            return super.configure(req, formData);
        }

        /**
         * This method returns true if the global configuration says we should speak French.
         * <p>
         * The method name is bit awkward because global.jelly calls this method to determine
         * the initial state of the checkbox by the naming convention.
         */
        public String getCasUrl() {
            return casUrl;
        }

        public String getCasPort() {
            return casPort;
        }
    }
}

