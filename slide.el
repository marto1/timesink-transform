;; Swideshow script - run things with a command and display them
;; in swideshow buffer in Emacs.
;;
;;FIXME make this into a mode so multiple instances can be ran
;;FIXME name of buffer not unique

(require 'url)

(defun insert-image-from-url (&optional url)
  (interactive)
  (unless url (setq url (url-get-url-at-point)))
  (unless url
    (error "Couldn't find URL."))
  (let ((buffer (url-retrieve-synchronously url)))
    (unwind-protect
         (let ((data (with-current-buffer buffer
                       (goto-char (point-min))
                       (search-forward "\n\n")
                       (buffer-substring (point) (point-max)))))
           (insert-image (create-image data nil t)))
      (kill-buffer buffer))))

;;set this to command that returns ((<link> <title>)...) sexp
(setq roll-lol-slideshow-command
      "python hugescrape.py --output=sexp")

;;go to next entry every <roll-lol-each> seconds 
(setq roll-lol-each 5)
(setq roll-lol-timer nil)

(defun roll-lol-entry (entry buf)
  "clean buffer and roll next entry"
  (switch-to-buffer buf)
  (erase-buffer)
  (message "lol - title:%s link:%s" (cadr entry) (car entry))
  (insert (cadr entry))
  (insert "\n")
  (insert-image-from-url (car entry))
  (insert "\n")
  (insert (car entry)))

(defun roll-lol-show ()
  (let ((lolbuf (get-buffer-create "lol-slideshow")))
    (switch-to-buffer lolbuf)
    (let* ((value)
	  (entry)
	  (data (car (read-from-string
		   (shell-command-to-string
		    roll-lol-slideshow-command))))
	  (data-len (length data)))
      (setq lol-curr-entry 0) ;;FIXME wtf am I doing, get closures
      (setq lol-data data)
      (setq lol-datal data-len)
      (setq lol-buf lolbuf)
      (setq roll-lol-timer (run-at-time roll-lol-each roll-lol-each
		     (lambda ()
		       (progn
			 (roll-lol-entry
			  (nth lol-curr-entry lol-data) lol-buf)
			 (if (equal lol-curr-entry (- lol-datal 1))
			     (setq lol-curr-entry 0)
			   (setq lol-curr-entry
				 (1+ lol-curr-entry))))))))))


(roll-lol-show)
