using UnityEngine;
using UnityEditor;
using System.Diagnostics;
using System.IO;

public class AudioClassifierWindow : EditorWindow
{
    private string classifierPath;
    private string inputFolderPath;
    private bool isProcessing = false;

    [MenuItem("Tools/Audio Classifier")]
    public static void ShowWindow()
    {
        GetWindow<AudioClassifierWindow>("Audio Classifier");
    }

    private void OnEnable()
    {
        classifierPath = Path.Combine(Application.dataPath, "AudioClassifier/AudioClassifier.exe");
    }

    private void OnGUI()
    {
        GUILayout.Label("Audio Classification Settings", EditorStyles.boldLabel);

        EditorGUI.BeginDisabledGroup(isProcessing);

        using (new EditorGUI.DisabledGroupScope(isProcessing))
        {
            inputFolderPath = EditorGUILayout.TextField("Input Folder", inputFolderPath);

            if (GUILayout.Button("Select Input Folder"))
            {
                inputFolderPath = EditorUtility.OpenFolderPanel("Select Input Folder", "", "");
            }

            EditorGUILayout.Space();

            if (GUILayout.Button("Run Classification"))
            {
                RunClassification();
            }
        }

        if (isProcessing)
        {
            EditorGUILayout.HelpBox("Processing audio files...", MessageType.Info);
        }
    }

    private async void RunClassification()
    {
        if (string.IsNullOrEmpty(inputFolderPath))
        {
            EditorUtility.DisplayDialog("Error", "Please select an input folder", "OK");
            return;
        }

        isProcessing = true;

        try
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = classifierPath;
            startInfo.Arguments = $"\"{inputFolderPath}\"";
            startInfo.UseShellExecute = false;
            startInfo.RedirectStandardOutput = true;
            startInfo.RedirectStandardError = true;
            startInfo.CreateNoWindow = true;

            using (Process process = Process.Start(startInfo))
            {
                string output = await process.StandardOutput.ReadToEndAsync();
                string error = await process.StandardError.ReadToEndAsync();
                process.WaitForExit();

                // Log the standard output
                if (!string.IsNullOrEmpty(output))
                {
                    UnityEngine.Debug.Log($"Classification Output:\n{output}");
                }

                // Check for actual errors vs TensorFlow warnings
                if (!string.IsNullOrEmpty(error))
                {
                    // Filter out common TensorFlow warnings and info messages
                    bool isActualError = !error.Contains("oneDNN custom operations") &&
                                       !error.Contains("WARNING:tensorflow") &&
                                       !error.Contains("TensorFlow binary is optimized");

                    if (isActualError)
                    {
                        UnityEngine.Debug.LogError($"Classification Error: {error}");
                        EditorUtility.DisplayDialog("Error", "An error occurred during classification. Check console for details.", "OK");
                    }
                    else
                    {
                        // Just log TensorFlow warnings as info
                        UnityEngine.Debug.Log($"TensorFlow Messages:\n{error}");
                    }
                }

                // Check if files were actually processed
                if (output.Contains("Classification Summary"))
                {
                    AssetDatabase.Refresh();
                    EditorUtility.DisplayDialog("Success", "Audio classification completed successfully!", "OK");
                }
            }
        }
        catch (System.Exception e)
        {
            UnityEngine.Debug.LogError($"Error running classifier: {e.Message}");
            EditorUtility.DisplayDialog("Error", "Failed to run the classifier. Check console for details.", "OK");
        }
        finally
        {
            isProcessing = false;
        }
    }
}
