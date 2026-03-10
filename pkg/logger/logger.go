package logger

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
)

var ErrorLog *log.Logger

func Init(target string) {
	logDir := filepath.Join("logs", target)
	os.MkdirAll(logDir, 0755)

	logFile, err := os.OpenFile(filepath.Join(logDir, "errors.log"), os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		fmt.Printf("Fatal: Could not open log file: %v\n", err)
	}

	ErrorLog = log.New(logFile, "ERROR: ", log.Ldate|log.Ltime|log.Lshortfile)
}

func LogError(message string) {
	if ErrorLog != nil {
		ErrorLog.Println(message)
	}
}
func LogInfo(message string) {
	if ErrorLog != nil {
		ErrorLog.Println("INFO: " + message)
	}
}
