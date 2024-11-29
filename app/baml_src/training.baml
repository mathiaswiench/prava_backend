// Defining a data model.
class TrainingPlan {
  training Week[]
}

class Week {
  week int
  training Training[]
}

class Training {
  day string
  activity string
  targetPace float
  length float

}

class Activity {
    fileId int | string
    fileName string
    duration string | int | float
    distance float | string
    activityType string
    calories int | string
    ascent int | string
    avgPace string 
    minHeartRate int | string
    maxHeartRate int | string
    avgHeartRate int | string
    timeFinished string
}

// Create a function to extract the resume from a string.
function TrainingPlanGenerator(training_data: Activity[]) -> TrainingPlan {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client "openai/gpt-4o" // Set OPENAI_API_KEY to use this client.
  prompt #"
    You are a running coach. The person you want to coach has the goal to complete a marathon.
    The person wants to run the marathon in 4 hours and 30 minutes.
    Based on his training data, you want to create a Traiing Plan for 12 weeks.
    Training data:

    {{training_data}}

    {{ ctx.output_format }}
  "#
}

// Test the function with a sample resume. Open the VSCode playground to run this.
test TrainingPlanGenerator {
  functions [TrainingPlanGenerator]
  args {
    training_data [
      {
        fileId "21"
        fileName "activity_2024-10-07.csv"
        duration "01:14:13"
        distance 12.24
        activityType "Laufen"
        calories 781
        ascent 23
        avgPace "6:03"
        minHeartRate 0
        maxHeartRate 165
        avgHeartRate 143
        timeFinished "2024-10-07 07:13:07"
      }
      {
        fileId "22"
        fileName "activity_2024-10-04.csv"
        duration "01:10:08"
        distance 10.76
        activityType "Laufen"
        calories 755
        ascent 50
        avgPace "6:08"
        minHeartRate 0
        maxHeartRate 171
        avgHeartRate 147
        timeFinished "2024-10-04 14:25:26"
      }
      {
        fileId "23"
        fileName "activity_2024-10-01.csv"
        duration "00:38:02"
        distance 7.17
        activityType "Laufen"
        calories 432
        ascent 32
        avgPace "5:18"
        minHeartRate 0
        maxHeartRate 186
        avgHeartRate 154
        timeFinished "2024-10-01 18:22:46"
      }
      {
        fileId "24"
        fileName "activity_2024-09-30.csv"
        duration "00:43:40"
        distance 6.06
        activityType "Laufen"
        calories 417
        ascent 10
        avgPace "6:36"
        minHeartRate 0
        maxHeartRate 162
        avgHeartRate 140
        timeFinished "2024-09-30 18:04:46"
      }
    ]
  }
}
