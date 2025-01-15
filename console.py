def save_console_output_to_file(build_number, output_file):
    """
    Fetches console output in chunks and writes it to a file.
    """
    console_offset = 0

    with open(output_file, "w") as file:
        while True:
            # Fetch console output starting from the last offset
            console_output = server.get_build_console_output(JENKINS_JOB_NAME, build_number, start=console_offset)
            console_lines = console_output.splitlines()

            # Write lines to the file
            file.writelines(line + "\n" for line in console_lines)

            # If no new lines are available, stop
            if len(console_lines) == 0:
                break

            # Update offset for the next chunk
            console_offset += len(console_lines)

    print(f"Console output saved to {output_file}")



def main(jira_issue_key, param1, param2, param3):
    # Trigger Jenkins job with parameters
    jenkins_parameters = {
        "PARAM1": param1,
        "PARAM2": param2,
        "PARAM3": param3,
    }
    queue_item_number = trigger_jenkins_job(jenkins_parameters)

    # Get build number from queue item
    build_number = get_build_number_from_queue(queue_item_number)

    # Wait for build to complete
    build_info = wait_for_build_to_complete(build_number)

    # Save console output to a file
    output_file = f"build_{build_number}_console_output.txt"
    save_console_output_to_file(build_number, output_file)

    # Extract final image path
    final_image_path = get_final_image_path(build_number)
    if final_image_path:
        print(f"Final image path: {final_image_path}")

        # Comment the path in Jira
        comment = f"The final image is available at: {final_image_path}"
        comment_on_jira(jira_issue_key, comment)