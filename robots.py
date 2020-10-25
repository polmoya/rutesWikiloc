from urllib import robotparser
from urllib import parse
import constants

robot_parser = robotparser.RobotFileParser()

def prepare (robots_txt_url):
    print (robots_txt_url);
    #Sets tre URL referring to a robots.txt file
    robot_parser.set_url(robots_txt_url);
    #Reads the robots.txt URL and feeds it to the parser
    robot_parser.read();
    print ("File " + robots_txt_url + " readed...");

def is_allowed (target_url, user_agent='*'):
    isAllow:bool = False;
    
    #can_fetch()
    #returns True if the useragent is allowed to fecth the url according to the rules contained in the parsed
    #robots.txt file
    isAllow = robot_parser.can_fetch(user_agent,target_url);
    if isAllow:
        print ("URL: " + target_url + " is allowed to scrap...");
    else:
        print ("URL: " + target_url + " is not allowed to scrap...");
    return isAllow;

if __name__ == '__main__':
    prepare(parse.urljoin(constants.MAIN_URL,constants.ROBOTS_FILE));
    is_allowed(parse.urljoin(constants.MAIN_URL,constants.RUTAS_PAGE));

"""
if __name__ == '__main__':
    prepare('https://hajba.hu/robots.txt');

print(is_allowed('https://hajba.hu/category/software-development/java-software-development/', 'bookbot'));
print(is_allowed('http://hajba.hu/category/software-development/java-software-development/', 'my-agent'));
print(is_allowed('http://hajba.hu/category/software-development/java-software-development/', 'googlebot'));
"""
