#20160211
#Normalizing course data

data <- read.csv("~/PycharmProjects/CourseTalk/data.csv", stringsAsFactors=FALSE); as.data.frame(data)

# Clean up noisy data - using review no.
clean_data <- data[which(data$course_rating <= 10), ]

# Get List of URLs
urls <- clean_data['course_url']
write.csv(urls, "~/PycharmProjects/CourseTalk/url_data.csv")






