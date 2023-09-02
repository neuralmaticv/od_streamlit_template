import time
import requests
from typing import BinaryIO, Tuple, Optional

import streamlit as st
import streamlit.components.v1 as components

from config import config
from stream.stream_capture import StreamCapture


def show_message(message: str, message_type: str, section: st.container) -> None:
    """Displays a message in a Streamlit container.

    Args:
        message (str): The message to be displayed.
        message_type (str): The type of message. Possible values are "success", "warning", or "error".
        section (st.container): The Streamlit container to display the message in.

    Returns:
        None
    """
    with section.container():
        if message_type == "success":
            st.success(message)
        elif message_type == "warning":
            st.warning(message)
        elif message_type == "error":
            st.error(message)

        time.sleep(3)
        section.empty()

def show_source(section: st.container, source_type: str, uploaded_file: BinaryIO, selected_camera: str) -> None:
    """Show the source of an image, video, or camera stream.

    Args:
        section: Streamlit container to display the source.
        source_type: Type of the source ("Image" for image, "Video" for video, "Stream" for camera stream).
        uploaded_file: BinaryIO object representing the uploaded file (for image or video sources).
        selected_camera: Name of the selected camera (for camera stream source).

    Returns:
        None

    Note:
        This function uses the StreamCapture class to capture frames from a camera stream.
    """
    if uploaded_file or selected_camera:
        with section.container():
            if source_type == "Image":
                st.image(uploaded_file.read(), use_column_width="always")
            elif source_type == "Video":
                st.video(uploaded_file.read())
            elif source_type == "Stream":
                username = config.STREAMS[selected_camera]["username"]
                password = config.STREAMS[selected_camera]["password"]
                addr = config.STREAMS[selected_camera]["address"]
                rtsp_port = config.STREAMS[selected_camera]["port"]
                endpoint = config.STREAMS[selected_camera]["endpoint"]
                rtsp_url = f"rtsp://{username}:{password}@{addr}:{rtsp_port}/{endpoint}"

                stframe = st.empty()
                stream = StreamCapture(rtsp_url)
                if st.button("Stop"):
                    stream.stop()

                while True:
                    frame = stream.read()
                    
                    if frame is None:
                        st.write("Error with rtsp")
                        break

                    stframe.image(frame, use_column_width="always")

def clear_section(section: st.container) -> None:
    """Clear a section in Streamlit.

    Args:
        section: The section to be cleared.

    Returns:
        None
    """
    section.empty()

def assign_task(selected_source: str, uploaded_file: BinaryIO, selected_camera: str, info_container: st.container, results_expander: st.expander, history_expander:st.expander) -> None:
    """Assign a task based on the selected source.

    Args:
        selected_source (str): The selected source ("Image", "Video", "Stream").
        uploaded_file (BinaryIO): The uploaded file.
        selected_camera (str): The selected camera.
        info_container (st.container): The container to display information messages.
        results_expander (st.expander): The expander to display results.
        history_expander (st.expander): The expander to display history.

    Returns:
        None
    """
    if selected_source == "Image":
        if uploaded_file is None:
            show_message("You haven't uploaded an image", "error", info_container)
        else:
            show_message("Model is running", "success", info_container)

            response = requests.post(
                f"cv/{config.API_ADDRESS}/infer_image",
                files={"file": uploaded_file},
            )

            if response.status_code == 200:
                with results_expander:
                    results_table, results_image = results_expander.columns(2)

                    results_table.json(response.json())
                    results_image.image(
                            uploaded_file, use_column_width="always")
            else:
                print("error")
    elif selected_source == "Video":
        if uploaded_file is None:
            show_message("You haven't uploaded a video", "error", info_container)
        else:
            show_message("Model is running", "success", info_container)
            
            response = requests.post(
                f"cv/{config.API_ADDRESS}/infer_video",
                files={"video": uploaded_file},
            )

            # TODO: handle video response
    elif selected_source == "Stream":
        if selected_camera == "":
            show_message("You haven't selected a camera stream", "error", info_container)
        else:
            show_message("Model is running", "success", info_container)

            url = f"cv/{config.API_ADDRESS}/{selected_camera}/infer_stream"
            with results_expander:
                # results_table, results_image = results_expander.columns(2)
                components.html(
                    f"""
                    <img src="{url}" width="1280" height="720" />
                    """,
                    width=1280,
                    height=720,
                )
    else:
        show_message("Invalid source", "error", info_container)

def save_parameters(selected_model: str, classes_to_include: list, confidence_threshold: float, iou_threshold: float, info_container: st.container) -> None:
    """Save parameters.

    Args:
        selected_model (str): The selected model.
        classes_to_include (list): The classes to include for recognition.
        confidence_threshold (float): The confidence threshold.
        iou_threshold (float): The NMS IOU threshold.
        info_container (st.container): The container to display information.

    Returns:
        None
    """
    if len(classes_to_include) == 0:
        show_message("You haven't selected any class for recognition",
                  "error", info_container)
    else:
        with info_container.container():
            st.write("---")
            st.write("### Config:")
            st.write(f"Model: {selected_model}")
            st.write(f"Classes: {classes_to_include}")
            st.write(f"Confidence threshold: {confidence_threshold}")
            st.write(f"NMS IOU threshold: {iou_threshold}")
            st.write("---")

        custom_config = None
        if selected_model == "SOME_MODEL":
            # TODO: handle model parameters and create custom_config
            pass

        response = requests.post(
            f"cv/{config.API_ADDRESS}/set_config",
            json=custom_config,
        )

        if response.status_code == 200:
            show_message("Model has been successfully configured", "success", info_container)

            print(response.json()["info"])
            print(response.json()["config"])
        else:
            show_message("Error while configuring the model", "error", info_container)

def setup_sidebar() -> None:
    """Setup the sidebar for model parameters selection in Streamlit."""
    with st.sidebar:
        model_selectbox = st.sidebar.selectbox(
            "Model",
            (model_name for model_name in config.MODELS.keys())
        )

        classes_to_include = st.multiselect(
            "Class",
            options=config.CLASSES,
            # TODO: handle default class
            default=[config.CLASSES["class_name"]]
        )

        confidence_threshold_slider = st.slider(
            "Confidence threshold",
            config.MIN_CONFIDENCE_THRESHOLD, config.MAX_CONFIDENCE_THRESHOLD, config.DEFAULT_CONFIDENCE_THRESHOLD, 0.05
        )

        iou_threshold_slider = st.slider(
            "NMS IOU threshold",
            config.MIN_IOU_THRESHOLD, config.MAX_IOU_THRESHOLD, config.DEFAULT_IOU_THRESHOLD, 0.05
        )

        info_container = st.empty()

        st.button("Save", key="save_parameters", help="Save model parameters", on_click=save_parameters, args=(
            model_selectbox, classes_to_include, confidence_threshold_slider, iou_threshold_slider, info_container))

def get_resource_selection() -> Tuple[str, Optional[BinaryIO], str]:
    """Get the resource selection from the user."""
    st.markdown("### Source selection:")
    left_column, right_column = st.columns(2)
    with left_column:
        source_selectbox = st.selectbox(
            "Choose a source",
            (source for source in config.SOURCES.keys())
        )
    
    camera_selectbox = ""
    uploaded_file = None
    with right_column:
        if source_selectbox == "Image":
            uploaded_file = st.file_uploader(
                "Upload image:", type=['png', 'jpg', 'jpeg'])
        elif source_selectbox == "Video":
            uploaded_file = st.file_uploader(
                "Upload video", type=['mp4'])
        elif source_selectbox == "Stream":
            camera_selectbox = st.selectbox(
                "Choose a camera/stream", (camera for camera in config.SOURCES["Stream"].keys()))

    return source_selectbox, uploaded_file, camera_selectbox


def main():
    """Main function.

    This function is the entry point of the program. It sets the page configuration, creates the sidebar for settings, 
    handles resource selection, and displays the preview, results, and history sections.

    Args:
        None

    Returns:
        None
    """
    st.set_page_config(page_title=config.PROJECT_NAME +
                       " APP", layout="wide")
    st.sidebar.title("Settings")

    setup_sidebar()

    selected_source, uploaded_file, selected_camera = get_resource_selection()

    preview_container = st.container()
    results_container = st.container()
    results_history = st.container()

    with preview_container:
        st.write("---")
        preview_container_title = st.container()
        dashboard_section, preview_section = st.columns(2)

    with results_container:
        results_container.write("---")
        results_container.markdown("### Inference results:")

        results_expander = results_container.expander("Show results")

    with results_history:
        st.markdown("#### History:")
        history_expander = results_history.expander("Show history")

    if selected_source != "":
        with preview_container_title:
            st.markdown("### Preview:")

        with dashboard_section:
            button1, button2 = st.columns(2)
            with button1:
                st.button("Show", key="show_source", help="Show selected resource",
                          on_click=show_source, args=(preview_section, selected_source, uploaded_file, selected_camera))
            with button2:
                st.button("Hide", key="clear_section", help="Hide selected resource",
                          on_click=clear_section, args=(preview_section,))

            run_button, dashboard_info_container = st.columns(2)
            dashboard_info_container = st.empty()

            with run_button:
                st.button("Run model", key="run_model", help="Run model on selected resource",
                          on_click=assign_task, args=(selected_source, uploaded_file, selected_camera, dashboard_info_container, results_expander, history_expander))


if __name__ == "__main__":
    main()
