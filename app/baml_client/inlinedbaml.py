###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> CustomGPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\n",
    "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.62.0\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode async\n}\n",
    "training.baml": "// Defining a data model.\nclass TrainingPlan {\n  training Week[]\n}\n\nclass Week {\n  week int\n  training Training[]\n}\n\nclass Training {\n  day string\n  activity string\n  targetPace float\n  length float\n\n}\n\nclass Activity {\n    fileId int | string\n    fileName string\n    duration string | int | float\n    distance float | string\n    activityType string\n    calories int | string\n    ascent int | string\n    avgPace string \n    minHeartRate int | string\n    maxHeartRate int | string\n    avgHeartRate int | string\n    timeFinished string\n}\n\n// Create a function to extract the resume from a string.\nfunction TrainingPlanGenerator(training_data: Activity[]) -> TrainingPlan {\n  // Specify a client as provider/model-name\n  // you can use custom LLM params with a custom client name from clients.baml like \"client CustomHaiku\"\n  client \"openai/gpt-4o\" // Set OPENAI_API_KEY to use this client.\n  prompt #\"\n    You are a running coach. The person you want to coach has the goal to complete a marathon.\n    The person wants to run the marathon in 4 hours and 30 minutes.\n    Based on his training data, you want to create a Traiing Plan for 12 weeks.\n    Training data:\n\n    {{training_data}}\n\n    {{ ctx.output_format }}\n  \"#\n}\n\n// Test the function with a sample resume. Open the VSCode playground to run this.\ntest TrainingPlanGenerator {\n  functions [TrainingPlanGenerator]\n  args {\n    training_data [\n      {\n        fileId \"21\"\n        fileName \"activity_2024-10-07.csv\"\n        duration \"01:14:13\"\n        distance 12.24\n        activityType \"Laufen\"\n        calories 781\n        ascent 23\n        avgPace \"6:03\"\n        minHeartRate 0\n        maxHeartRate 165\n        avgHeartRate 143\n        timeFinished \"2024-10-07 07:13:07\"\n      }\n      {\n        fileId \"22\"\n        fileName \"activity_2024-10-04.csv\"\n        duration \"01:10:08\"\n        distance 10.76\n        activityType \"Laufen\"\n        calories 755\n        ascent 50\n        avgPace \"6:08\"\n        minHeartRate 0\n        maxHeartRate 171\n        avgHeartRate 147\n        timeFinished \"2024-10-04 14:25:26\"\n      }\n      {\n        fileId \"23\"\n        fileName \"activity_2024-10-01.csv\"\n        duration \"00:38:02\"\n        distance 7.17\n        activityType \"Laufen\"\n        calories 432\n        ascent 32\n        avgPace \"5:18\"\n        minHeartRate 0\n        maxHeartRate 186\n        avgHeartRate 154\n        timeFinished \"2024-10-01 18:22:46\"\n      }\n      {\n        fileId \"24\"\n        fileName \"activity_2024-09-30.csv\"\n        duration \"00:43:40\"\n        distance 6.06\n        activityType \"Laufen\"\n        calories 417\n        ascent 10\n        avgPace \"6:36\"\n        minHeartRate 0\n        maxHeartRate 162\n        avgHeartRate 140\n        timeFinished \"2024-09-30 18:04:46\"\n      }\n    ]\n  }\n}\n",
}

def get_baml_files():
    return file_map