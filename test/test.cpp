#include <cpr/cpr.h>
#include <iostream>

int main() {
    // Define the URL and headers for the GET request
    std::string url = "https://webservices22.autotask.net/ATServicesRest/V1.0/ConfigurationItems/1";
    cpr::Header headers = {
        {"ApiIntegrationCode", "BGOMLNT67XY2BP2P4EIIU4DBK6K"},
        {"UserName", "eaxvwrkfllohdan@virtechsystemsSB060324.com"},
        {"Secret", "9p@Z#0LxR$g3*2AqyN~46#mGs"}
    };

    // Send the GET request
    cpr::Response r = cpr::Get(cpr::Url{url}, headers);

    // Check if the request was successful
    if (r.status_code == 200) {
        // Print the response content
        std::cout << "Response: " << r.text << std::endl;
    } else {
        // Print the error
        std::cout << "Failed to retrieve data. Status code: " << r.status_code << std::endl;
    }

    return 0;
}
