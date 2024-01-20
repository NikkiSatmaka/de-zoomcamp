variable "project" {
  description = "Project"
  default = "<PROJECT ID>"
}

variable "region" {
  description = "Region"
  default     = "ASIA-SOUTHEAST2"
}

variable "location" {
  description = "Project Location"
  default     = "ASIA-SOUTHEAST2"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "PROJECT-ID-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
